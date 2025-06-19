from langchain.tools import BaseTool
from typing import Optional, Dict, Any, Union
from pydantic import BaseModel, Field
import requests

class TMBaseToolInput(BaseModel):
    """Base input schema for Token Metrics tools."""
    pass

class TMBaseTool(BaseTool):
    """Base class for all Token Metrics tools."""
    
    def __init__(self, client):
        """Initialize the tool with a client instance.
        
        Args:
            client: TokenMetricsClient instance
        """
        super().__init__()
        self._client = client
        
    @property
    def client(self):
        """Get the client instance."""
        return self._client

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Make a GET request to the API.
        
        Args:
            path: API endpoint path
            params: Query parameters
            
        Returns:
            Response: The API response
        """
        url = f"{self.client.base_url}{path}"
        headers = {"Authorization": f"Bearer {self.client.api_key}"}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response

    def run(self, *args: Any, **kwargs: Any) -> str:
        """Run the tool with the given input.
        
        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            str: The tool's output
        """
        if len(args) == 1 and isinstance(args[0], dict):
            # If a single dictionary is passed, use it as kwargs
            kwargs = args[0]
        elif len(args) == 1 and isinstance(args[0], self.args_schema):
            # If a single input model is passed, convert it to kwargs
            kwargs = args[0].model_dump()
        return self._run(**kwargs)
        
    def _handle_error(self, error: Exception) -> str:
        """Handle errors in a consistent way across all tools.
        
        Args:
            error: The exception that was raised
            
        Returns:
            str: A user-friendly error message
        """
        if hasattr(error, 'response'):
            # Handle HTTP errors
            try:
                error_detail = error.response.json()
                return f"API Error: {error_detail.get('detail', str(error))}"
            except:
                return f"API Error: {str(error)}"
        return f"Error: {str(error)}" 