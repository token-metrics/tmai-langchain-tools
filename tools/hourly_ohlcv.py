from typing import Optional
from pydantic import Field
from datetime import datetime

from .base_tool import TMBaseTool, TMBaseToolInput

class HourlyOHLCVToolInput(TMBaseToolInput):
    """Input schema for the Hourly OHLCV tool."""
    token_id: Optional[str] = Field(
        None,
        description="Comma-separated Token IDs (e.g., '3375' for BTC)"
    )
    symbol: Optional[str] = Field(
        None,
        description="Comma-separated Token Symbols (e.g., 'BTC,ETH')"
    )
    token_name: Optional[str] = Field(
        None,
        description="Comma-separated Token Names (e.g., 'Bitcoin,Ethereum')"
    )
    start_date: Optional[str] = Field(
        None,
        description="Start date in YYYY-MM-DD format"
    )
    end_date: Optional[str] = Field(
        None,
        description="End date in YYYY-MM-DD format"
    )

class HourlyOHLCVTool(TMBaseTool):
    """Tool for accessing hourly OHLCV (Open, High, Low, Close, Volume) data."""
    
    name: str = "get_hourly_ohlcv"
    description: str = """Get hourly OHLCV (Open, High, Low, Close, Volume) data for cryptocurrencies.
    Useful when you need to:
    - Analyze historical price data on an hourly basis
    - Get detailed intraday trading volume information
    - Track short-term price movements
    - Perform technical analysis with higher granularity
    
    You can filter by:
    - token_id: Comma-separated Token IDs (e.g., "3375" for BTC)
    - symbol: Comma-separated Token Symbols (e.g., "BTC,ETH")
    - token_name: Comma-separated Token Names (e.g., "Bitcoin,Ethereum")
    - start_date: Start date in YYYY-MM-DD format
    - end_date: End date in YYYY-MM-DD format
    
    Note: Due to API limitations, data is limited to 29-day periods at a time.
    """
    args_schema = HourlyOHLCVToolInput

    def _run(
        self,
        token_id: Optional[str] = None,
        symbol: Optional[str] = None,
        token_name: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> str:
        """Run the tool to get hourly OHLCV data.
        
        Args:
            token_id: Comma-separated Token IDs (e.g., "3375" for BTC)
            symbol: Comma-separated Token Symbols (e.g., "BTC,ETH")
            token_name: Comma-separated Token Names (e.g., "Bitcoin,Ethereum")
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            str: A formatted string containing the hourly OHLCV data
        """
        try:
            # Validate dates if provided
            if start_date:
                try:
                    datetime.strptime(start_date, "%Y-%m-%d")
                except ValueError:
                    return "Error: start_date must be in YYYY-MM-DD format"
            
            if end_date:
                try:
                    datetime.strptime(end_date, "%Y-%m-%d")
                except ValueError:
                    return "Error: end_date must be in YYYY-MM-DD format"
            
            params = {
                'token_id': token_id,
                'symbol': symbol,
                'token_name': token_name,
                'start_date': start_date,
                'end_date': end_date
            }
            
            # Remove None values
            params = {k: v for k, v in params.items() if v is not None}
            
            response = self.client.base_endpoint._request("get", "/hourly-ohlcv", params=params)
            
            # Format the response as a readable string
            if isinstance(response, dict) and 'data' in response:
                ohlcv_data = response['data']
                if not ohlcv_data:
                    return "No hourly OHLCV data found for the specified criteria."
                
                result = []
                for entry in ohlcv_data:
                    ohlcv_info = [                        
                        f"TOKEN_ID: {entry.get('TOKEN_ID', 'Unknown')}",
                        f"TOKEN_NAME: {entry.get('TOKEN_NAME', 'Unknown')}",
                        f"TOKEN_SYMBOL: {entry.get('TOKEN_SYMBOL', 'Unknown')}",
                        f"Date/Hour: {entry.get('TIMESTAMP', 'Unknown')}",
                        f"Open: ${entry.get('OPEN', 'Unknown')}",
                        f"High: ${entry.get('HIGH', 'Unknown')}",
                        f"Low: ${entry.get('LOW', 'Unknown')}",
                        f"Close: ${entry.get('CLOSE', 'Unknown')}",
                        f"Volume: {entry.get('VOLUME', 'Unknown')}"
                    ]
                    result.append("\n".join(ohlcv_info))
                
                return "\n\n".join(result)
            
            return str(response)
            
        except Exception as e:
            return self._handle_error(e)
    
    def _arun(self, **kwargs) -> str:
        """Async implementation of the tool (not implemented)."""
        raise NotImplementedError("Async version not implemented")
