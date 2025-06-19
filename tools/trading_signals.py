from typing import Optional
from pydantic import Field
from datetime import datetime

from .base_tool import TMBaseTool, TMBaseToolInput

class TradingSignalsToolInput(TMBaseToolInput):
    """Input schema for the Trading Signals tool."""
    token_id: Optional[str] = Field(
        None,
        description="Comma-separated Token IDs (e.g., '3375' for BTC)"
    )
    symbol: Optional[str] = Field(
        None,
        description="Comma-separated Token Symbols (e.g., 'BTC,ETH')"
    )
    start_date: Optional[str] = Field(
        None,
        description="Start date in YYYY-MM-DD format"
    )
    end_date: Optional[str] = Field(
        None,
        description="End date in YYYY-MM-DD format"
    )
    category: Optional[str] = Field(
        None,
        description="Comma-separated category names (e.g., 'layer-1,nft')"
    )
    exchange: Optional[str] = Field(
        None,
        description="Comma-separated exchange names (e.g., 'binance,gate')"
    )
    marketcap: Optional[str] = Field(
        None,
        description="Minimum MarketCap in $"
    )
    volume: Optional[str] = Field(
        None,
        description="Minimum 24h trading volume in $"
    )
    fdv: Optional[str] = Field(
        None,
        description="Minimum fully diluted valuation in $"
    )
    signal: Optional[str] = Field(
        None,
        description="Signal value: bullish (1), bearish (-1) or no signal (0)"
    )

class TradingSignalsTool(TMBaseTool):
    """Tool for accessing AI-generated trading signals from Token Metrics."""
    
    name: str = "get_trading_signals"
    description: str = """Get AI-generated trading signals for cryptocurrencies to identify potential buying and selling opportunities.
    Useful when you need to:
    - Get AI-powered trading recommendations
    - Identify potential long and short positions
    - Filter signals by various criteria
    - Track trading signals over time
    
    You can filter signals by:
    - token_id: Comma-separated Token IDs
    - symbol: Token symbols
    - category: Token categories (e.g., "layer-1,nft")
    - exchange: Exchange names
    - marketcap: Minimum market cap
    - volume: Minimum 24h volume
    - fdv: Minimum fully diluted value
    - signal: Specific signal type (1 for bullish, -1 for bearish, 0 for no signal)
    - start_date/end_date: Date range
    
    Note: Data is limited to 29-day periods at a time.
    """
    args_schema = TradingSignalsToolInput

    def _run(
        self,
        token_id: Optional[str] = None,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        category: Optional[str] = None,
        exchange: Optional[str] = None,
        marketcap: Optional[str] = None,
        volume: Optional[str] = None,
        fdv: Optional[str] = None,
        signal: Optional[str] = None
    ) -> str:
        """Run the tool to get trading signals data.
        
        Args:
            token_id: Comma-separated Token IDs (e.g., "3375" for BTC)
            symbol: Comma-separated Token Symbols (e.g., "BTC,ETH")
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            category: Comma-separated category names (e.g., "layer-1,nft")
            exchange: Comma-separated exchange names (e.g., "binance,gate")
            marketcap: Minimum MarketCap in $
            volume: Minimum 24h trading volume in $
            fdv: Minimum fully diluted valuation in $
            signal: Signal value: bullish (1), bearish (-1) or no signal (0)
            
        Returns:
            str: A formatted string containing the trading signals data
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
                'start_date': start_date,
                'end_date': end_date,
                'category': category,
                'exchange': exchange,
                'marketcap': marketcap,
                'volume': volume,
                'fdv': fdv,
                'signal': signal
            }
            
            # Remove None values
            params = {k: v for k, v in params.items() if v is not None}
            
            response = self.client.base_endpoint._request("get", "/trading-signals", params=params)
            
            # Format the response as a readable string
            if isinstance(response, dict) and 'data' in response:
                data = response['data']
                if not data:
                    return "No market metrics data found for the specified criteria."
                
                
                result = []
                for entry in data:
                    signal_info = [
                        f"Token ID: {entry.get('TOKEN_ID', 0)}",
                        f"Token: {entry.get('TOKEN_NAME', 'Unknown')} ({entry.get('TOKEN_SYMBOL', 'Unknown')})",
                        f"Date: {entry.get('DATE', 'Unknown')}",
                        f"Signal: {entry.get('TRADING_SIGNAL', 'Unknown')}",
                        f"Token Trend: {entry.get('TOKEN_TREND', 0)}",
                        f"Trading Signal Returns: {entry.get('TRADING_SIGNALS_RETURNS', 0)}",
                        f"Holding Returns: {entry.get('HOLDING_RETURNS', 0)}",
                        f"TM Link: {entry.get('tm_link', 'Unknown')}",
                        "\nGrades:",
                        f"- TM Trader Grade: {entry.get('TM_TRADER_GRADE', 0)}",
                        f"- TM Investor Grade: {entry.get('TM_INVESTOR_GRADE', 0)}",
                        f"TM Link: {entry.get('TM_LINK', 'Unknown')}"
                    ]
                    result.append("\n".join(signal_info))
                
                return "\n\n".join(result)
            
            return str(response)
            
        except Exception as e:
            return self._handle_error(e)
    
    def _arun(self, **kwargs) -> str:
        """Async implementation of the tool (not implemented)."""
        raise NotImplementedError("Async version not implemented")