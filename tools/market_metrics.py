from typing import Optional
from pydantic import Field
from datetime import datetime

from .base_tool import TMBaseTool, TMBaseToolInput

class MarketMetricsToolInput(TMBaseToolInput):
    """Input schema for the Market Metrics tool."""
    start_date: Optional[str] = Field(
        None,
        description="Start date in YYYY-MM-DD format"
    )
    end_date: Optional[str] = Field(
        None,
        description="End date in YYYY-MM-DD format"
    )
    limit: Optional[int] = Field(
        50,
        description="Limit the number of results to return"
    )
    page: Optional[int] = Field(
        1,
        description="Page number for pagination"
    )

class MarketMetricsTool(TMBaseTool):
    """Tool for accessing market sentiment metrics from Token Metrics."""
    
    name: str = "get_market_metrics"
    description: str = """Get comprehensive market analytics and sentiment metrics for the entire cryptocurrency market.
    Useful when you need to:
    - Understand overall market sentiment
    - Track market bullish/bearish indicators
    - Monitor market volatility
    - Analyze market momentum
    
    The tool provides various metrics including:
    - Market Sentiment: Overall market sentiment indicator
    - Bullish/Bearish Indicator: Market direction indicator
    - Market Volatility: Volatility metrics
    - Market Momentum: Momentum indicators
    
    You can specify a date range using:
    - start_date: Start date in YYYY-MM-DD format
    - end_date: End date in YYYY-MM-DD format
    
    Note: Data is limited to 29-day periods at a time.
    """
    args_schema = MarketMetricsToolInput

    def _run(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None
    ) -> str:
        """Run the tool to get market metrics data.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            limit: Limit the number of results to return
            page: Page number for pagination
            
        Returns:
            str: A formatted string containing the market metrics data
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
                'start_date': start_date,
                'end_date': end_date
            }
            
            # Remove None values
            params = {k: v for k, v in params.items() if v is not None}
            
            response = self.client.base_endpoint._request("get", "/market-metrics", params=params)
            
            # Format the response as a readable string
            if isinstance(response, dict) and 'data' in response:
                metrics_data = response['data']
                if not metrics_data:
                    return "No market metrics data found for the specified criteria."
                
                result = []
                for entry in metrics_data:
                    metrics_info = [
                        f"Date: {entry.get('DATE', 'Unknown')}",
                        f"Total Crypto Market Cap: {entry.get('TOTAL_CRYPTO_MCAP', 0)}",
                        f"High Grade Coins %: {entry.get('TM_GRADE_PERC_HIGH_COINS', 0)}",
                        f"TM Grade Signal: {entry.get('TM_GRADE_SIGNAL', 0)}",
                        f"Last TM Grade Signal: {entry.get('LAST_TM_GRADE_SIGNAL', 0)}"
                    ]
                    result.append("\n".join(metrics_info))
                
                return "\n\n".join(result)
            
            return str(response)
            
        except Exception as e:
            return self._handle_error(e)
    
    def _arun(self, **kwargs) -> str:
        """Async implementation of the tool (not implemented)."""
        raise NotImplementedError("Async version not implemented")
