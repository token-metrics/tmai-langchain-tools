import requests
import pandas as pd
import datetime
from tqdm import tqdm
import logging
import json
from typing import Dict, Any, Optional

# Configure logging
logger = logging.getLogger(__name__)

class BaseEndpoint:
    """Base class for all API endpoints"""
    
    def __init__(self, client):
        """Initialize the endpoint with a client instance.
        
        Args:
            client: TokenMetricsClient instance
        """
        self.client = client
        self.base_url = client.BASE_URL
    
    def _request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a request to the API.
        
        Args:
            method (str): HTTP method (get, post, etc.)
            endpoint (str): API endpoint path
            params (dict, optional): Query parameters for GET requests
            json_data (dict, optional): JSON payload for POST requests
            
        Returns:
            dict: API response data
            
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "accept": "application/json",
            "x-api-key": self.client.api_key,
            "x-integration": "langchain"
        }
        
        # Log request details
        logger.debug(f"Making {method.upper()} request to {url}")
        logger.debug(f"Headers: {json.dumps({k: '***' if k == 'x-api-key' else v for k, v in headers.items()})}")
        logger.debug(f"Params: {json.dumps(params) if params else None}")
        
        try:
            if method.lower() == "get":
                response = requests.get(url, headers=headers, params=params)
            elif method.lower() == "post":
                headers["content-type"] = "application/json"
                response = requests.post(url, headers=headers, json=json_data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Log response details
            logger.debug(f"Response status code: {response.status_code}")
            logger.debug(f"Response headers: {dict(response.headers)}")
            
            if response.status_code >= 400:
                logger.error(f"Request failed with status {response.status_code}")
                logger.error(f"Response body: {response.text}")
                
            # Raise an exception if the request failed
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status code: {e.response.status_code}")
                logger.error(f"Response headers: {dict(e.response.headers)}")
                logger.error(f"Response body: {e.response.text}")
            raise
    
    def _chunk_date_range(self, startDate, endDate, max_days=29):
        """Split a date range into chunks of max_days.
        
        Args:
            startDate (str): Start date in YYYY-MM-DD format
            endDate (str): End date in YYYY-MM-DD format
            max_days (int): Maximum number of days in each chunk
            
        Returns:
            list: List of (chunk_start_date, chunk_end_date) tuples
        """
        if not startDate or not endDate:
            return [(startDate, endDate)]  # If dates not provided, return as is
            
        try:
            start = datetime.datetime.strptime(startDate, "%Y-%m-%d")
            end = datetime.datetime.strptime(endDate, "%Y-%m-%d")
        except ValueError:
            # If date parsing fails, return as is
            return [(startDate, endDate)]
            
        # Check if the range is already within limits
        if (end - start).days <= max_days:
            return [(startDate, endDate)]
            
        # Split into chunks
        result = []
        chunk_start = start
        
        while chunk_start < end:
            # Calculate chunk end date (chunk_start + max_days or end date, whichever is earlier)
            chunk_end = min(chunk_start + datetime.timedelta(days=max_days), end)
            
            # Add to result as strings
            result.append((
                chunk_start.strftime("%Y-%m-%d"),
                chunk_end.strftime("%Y-%m-%d")
            ))
            
            # Move to next chunk
            chunk_start = chunk_end
            
        return result
    
    def _paginated_request(self, method, endpoint, params=None, max_days=29, custom_limit=None):
        """Make paginated requests to handle date ranges and custom pagination logic.
        
        This method handles two forms of pagination:
        1. Date chunking: Splitting long date ranges into <= max_days chunks
        2. Offset-based pagination: Since the API's page parameter doesn't work as expected
        
        Args:
            method (str): HTTP method (get, post, etc.)
            endpoint (str): API endpoint path
            params (dict): Query parameters including startDate and endDate
            max_days (int): Maximum number of days allowed between startDate and endDate
            custom_limit (int, optional): Custom limit value. If None, uses endpoint-specific defaults.
            
        Returns:
            dict: Combined API response data
        """
        # Default limits for different endpoints
        endpoint_limits = {
            'daily-ohlcv': 100,
            'hourly-ohlcv': 1000,
            'trader-grades': 1000,
            'investor-grades': 1000,
            'market-metrics': 1000,
            'trader-indices': 1000,
            'trading-signals': 1000,
            # Default for any other endpoint
            'default': 1000
        }
        if params is None:
            params = {}
            
        # Extract date parameters
        startDate = params.get('startDate')
        endDate = params.get('endDate')
        
        # Determine the limit to use
        if custom_limit is not None:
            limit = custom_limit
        else:
            # Use endpoint-specific limit
            limit = endpoint_limits.get(endpoint, endpoint_limits['default'])
        
        # Override user-provided limit with our internal limit
        params['limit'] = limit
        
        # We'll remove page parameter since we're handling pagination ourselves
        if 'page' in params:
            del params['page']
            
        # If no date range or already within limits, we still need to handle pagination
        if not startDate or not endDate:
            date_chunks = [(startDate, endDate)]
        else:
            # Split date range into chunks
            date_chunks = self._chunk_date_range(startDate, endDate, max_days)
        
        # Initialize combined results
        all_data = []
        combined_meta = {}
        
        # Calculate total iterations for progress bar
        total_iterations = len(date_chunks)
        
        # Setup progress bar
        with tqdm(total=total_iterations, desc=f"Fetching {endpoint} data", unit="chunk") as pbar:
            # Process each date chunk
            for chunk_start, chunk_end in date_chunks:
                # Update date parameters
                chunk_params = params.copy()
                if chunk_start:
                    chunk_params['startDate'] = chunk_start
                if chunk_end:
                    chunk_params['endDate'] = chunk_end
                
                # Set a high limit to get as much data as possible in one request
                chunk_params['limit'] = limit
                
                # Always start with page 0 for each chunk
                chunk_params['page'] = 0
                
                # Make the request
                response = self._request(method, endpoint, chunk_params)
                
                # Extract data and metadata
                if isinstance(response, dict):
                    data = response.get('data', [])
                    meta = {k: v for k, v in response.items() if k != 'data'}
                    if meta:
                        combined_meta.update(meta)
                else:
                    data = response
                
                # Add data to combined results
                if data:
                    all_data.extend(data)
                
                # Update progress bar
                pbar.update(1)
            
        # Construct the final response
        if combined_meta:
            result = combined_meta.copy()
            result["data"] = all_data
            return result
        elif all_data and isinstance(all_data[0], dict):
            # If we have data items and they're dictionaries, return in standard format
            return {"data": all_data}
        else:
            # Otherwise, return just the data array
            return all_data
    
    def to_dataframe(self, data):
        """Convert API response data to a pandas DataFrame.
        
        Args:
            data (dict): API response data
            
        Returns:
            pandas.DataFrame: DataFrame containing the response data
        """
        # Implementation depends on the specific structure of each endpoint's response
        # This is a placeholder to be overridden by subclasses
        if isinstance(data, list):
            if not data:  # Handle empty list
                return pd.DataFrame()
            return pd.DataFrame(data)
        elif isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
            if not data["data"]:  # Handle empty data array
                return pd.DataFrame()
            return pd.DataFrame(data["data"])
        else:
            return pd.DataFrame([data])
