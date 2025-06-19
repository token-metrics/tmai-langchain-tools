from typing import Optional
from pydantic import Field
from datetime import datetime

from .base_tool import TMBaseTool, TMBaseToolInput

class DailyOHLCVToolInput(TMBaseToolInput):
    """Input schema for the Daily OHLCV tool."""
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

class DailyOHLCVTool(TMBaseTool):
    """Tool for accessing daily OHLCV (Open, High, Low, Close, Volume) data."""
    
    name: str = "get_daily_ohlcv"
    description: str = """Get daily OHLCV (Open, High, Low, Close, Volume) data for cryptocurrencies.
    Useful when you need to:
    - Analyze historical price data on a daily basis
    - Get trading volume information
    - Track price movements over time
    - Perform technical analysis
    
    You can filter by:
    - token_id: Comma-separated Token IDs (e.g., "3375" for BTC)
    - symbol: Comma-separated Token Symbols (e.g., "BTC,ETH")
    - token_name: Comma-separated Token Names (e.g., "Bitcoin,Ethereum")
    - start_date: Start date in YYYY-MM-DD format
    - end_date: End date in YYYY-MM-DD format
    """
    args_schema = DailyOHLCVToolInput

    def _run(
        self,
        token_id: Optional[str] = None,
        symbol: Optional[str] = None,
        token_name: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> str:
        """Run the tool to get daily OHLCV data.
        
        Args:
            token_id: Comma-separated Token IDs (e.g., "3375" for BTC)
            symbol: Comma-separated Token Symbols (e.g., "BTC,ETH")
            token_name: Comma-separated Token Names (e.g., "Bitcoin,Ethereum")
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            str: A formatted string containing the daily OHLCV data
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
            
            response = self.client.base_endpoint._request("get", "/daily-ohlcv", params=params)
            
            # Format the response as a readable string
            if isinstance(response, dict) and 'data' in response:
                data = response['data']
                if not data:
                    return "No trader grades data found for the specified criteria."
                
                result = []
                for entry in data:
                    grades_info = [
                        f"Token ID: {entry.get('TOKEN_ID', 0)}",
                        f"Token: {entry.get('TOKEN_NAME', 'Unknown')} ({entry.get('TOKEN_SYMBOL', 'Unknown')})",
                        f"Date: {entry.get('DATE', 'Unknown')}",
                        f"Open: ${entry.get('OPEN', 0)}",
                        f"High: ${entry.get('HIGH', 0)}",
                        f"Low: ${entry.get('LOW', 0)}",
                        f"Close: ${entry.get('CLOSE', 0)}",
                        f"Volume: {entry.get('VOLUME', 0)}"
                    ]
                    result.append("\n".join(grades_info))
                
                return "\n\n".join(result)
            
            return str(response)
            
        except Exception as e:
            return self._handle_error(e)
    
    def _arun(self, **kwargs) -> str:
        """Async implementation of the tool (not implemented)."""
        raise NotImplementedError("Async version not implemented")