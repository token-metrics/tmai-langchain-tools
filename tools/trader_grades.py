from typing import Optional
from pydantic import Field
from datetime import datetime

from .base_tool import TMBaseTool, TMBaseToolInput

class TraderGradesToolInput(TMBaseToolInput):
    """Input schema for the Trader Grades tool."""
    token_id: Optional[str] = Field(
        None,
        description="Comma-separated Token IDs (e.g., '3375' for BTC)"
    )
    start_date: Optional[str] = Field(
        None,
        description="Start date in YYYY-MM-DD format"
    )
    end_date: Optional[str] = Field(
        None,
        description="End date in YYYY-MM-DD format"
    )
    symbol: Optional[str] = Field(
        None,
        description="Comma-separated Token Symbols (e.g., 'BTC,ETH')"
    )
    category: Optional[str] = Field(
        None,
        description="Comma-separated category names"
    )
    exchange: Optional[str] = Field(
        None,
        description="Comma-separated exchange names"
    )
    marketcap: Optional[str] = Field(
        None,
        description="Minimum MarketCap in $"
    )
    fdv: Optional[str] = Field(
        None,
        description="Minimum fully diluted valuation in $"
    )
    volume: Optional[str] = Field(
        None,
        description="Minimum 24h trading volume in $"
    )
    trader_grade: Optional[str] = Field(
        None,
        description="Minimum TM Trader Grade"
    )
    trader_grade_percent_change: Optional[str] = Field(
        None,
        description="Minimum 24h percent change in TM Trader Grade"
    )

class TraderGradesTool(TMBaseTool):
    """Tool for accessing short-term trading grades from Token Metrics."""
    
    name: str = "get_trader_grades"
    description: str = """Get short-term trading grades for cryptocurrencies to make informed buy and sell decisions.
    Useful when you need to:
    - Make short-term trading decisions
    - Analyze technical indicators
    - Evaluate quantitative performance metrics
    - Track trading grade changes
    
    The tool provides various grades including:
    - TM Trader Grade: Overall short-term trading outlook
    - TA Grade: Technical Analysis (price moves and trading indicators)
    - Quant Grade: Quantitative-Driven Performance Metrics
    - 24h Grade Change: Recent grade momentum
    
    You can filter by:
    - token_id: Comma-separated Token IDs
    - symbol: Token symbols
    - category: Token categories
    - exchange: Exchange names
    - marketcap: Minimum market cap
    - fdv: Minimum fully diluted value
    - volume: Minimum 24h volume
    - trader_grade: Minimum grade
    - trader_grade_percent_change: Minimum 24h change
    - start_date/end_date: Date range
    
    Note: Data is limited to 29-day periods at a time.
    """
    args_schema = TraderGradesToolInput

    def _run(
        self,
        token_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        symbol: Optional[str] = None,
        category: Optional[str] = None,
        exchange: Optional[str] = None,
        marketcap: Optional[str] = None,
        fdv: Optional[str] = None,
        volume: Optional[str] = None,
        trader_grade: Optional[str] = None,
        trader_grade_percent_change: Optional[str] = None
    ) -> str:
        """Run the tool to get trader grades data.
        
        Args:
            token_id: Comma-separated Token IDs (e.g., "3375" for BTC)
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            symbol: Comma-separated Token Symbols (e.g., "BTC,ETH")
            category: Comma-separated category names
            exchange: Comma-separated exchange names
            marketcap: Minimum MarketCap in $
            fdv: Minimum fully diluted valuation in $
            volume: Minimum 24h trading volume in $
            trader_grade: Minimum TM Trader Grade
            trader_grade_percent_change: Minimum 24h percent change in TM Trader Grade
            
        Returns:
            str: A formatted string containing the trader grades data
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
                'start_date': start_date,
                'end_date': end_date,
                'symbol': symbol,
                'category': category,
                'exchange': exchange,
                'marketcap': marketcap,
                'fdv': fdv,
                'volume': volume,
                'trader_grade': trader_grade,
                'trader_grade_percent_change': trader_grade_percent_change
            }
            
            # Remove None values
            params = {k: v for k, v in params.items() if v is not None}
            
            response = self.client.base_endpoint._request("get", "/trader-grades", params=params)
            
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
                        f"TM Trader Grade: {entry.get('TM_TRADER_GRADE', 0)}",
                        f"24h Change: {entry.get('TM_TRADER_GRADE_24H_PCT_CHANGE', 0)}%",
                        "\nGrades:",
                        f"- Technical Analysis: {entry.get('TA_GRADE', 0)}",
                        f"- Quantitative: {entry.get('QUANT_GRADE', 0)}"
                    ]
                    result.append("\n".join(grades_info))
                
                return "\n\n".join(result)
            
            return str(response)
            
        except Exception as e:
            return self._handle_error(e)
    
    def _arun(self, **kwargs) -> str:
        """Async implementation of the tool (not implemented)."""
        raise NotImplementedError("Async version not implemented")
