from typing import Optional
from pydantic import Field, validator
from datetime import datetime

from .base_tool import TMBaseTool, TMBaseToolInput

class ResistanceSupportToolInput(TMBaseToolInput):
    """Input schema for the Resistance and Support Levels tool."""
    token_id: Optional[str] = Field(
        None,
        description="Comma-separated Token IDs (e.g., '3375' for BTC)"
    )
    symbol: Optional[str] = Field(
        None,
        description="Comma-separated Token Symbols (e.g., 'BTC,ETH')"
    )
    limit: Optional[int] = Field(
        50,
        description="Limit the number of items in response"
    )
    page: Optional[int] = Field(
        1,
        description="Page number for pagination"
    )
   
class ResistanceSupportTool(TMBaseTool):
    """Tool for analyzing resistance and support levels in cryptocurrency markets."""
    
    name: str = "analyze_resistance_support_levels"
    description: str = """Analyze historical and current resistance and support levels for cryptocurrencies.
    Useful when you need to:
    - Identify key price levels for trading
    - Analyze historical support and resistance zones
    - Plan entry and exit points
    - Understand price action dynamics
    - Evaluate breakout/breakdown potential
    - Study market structure
    
    The tool provides detailed level analysis including:
    - Price levels
    - Level strength
    - Historical significance
    - Level type (support/resistance)
    - Time-based patterns
    - Market context
    
    You can analyze:
    - Multiple tokens at once
    - Historical patterns
    - Level strength
    - Price clusters
    - Breakout points
    - Market structure
    
    Filter options:
    - token_id: Comma-separated Token IDs (e.g., '3375' for BTC)
    - symbol: Token symbols (e.g., 'BTC,ETH')
    - limit: Number of records (default: 1000)
    - page: Pagination page (default: 1)
    """
    args_schema = ResistanceSupportToolInput

    def _run(
        self,
        token_id: Optional[str] = None,
        symbol: Optional[str] = None,
        limit: Optional[int] = 50,
        page: Optional[int] = 1
    ) -> str:
        """Run the tool to analyze resistance and support levels.
        
        Args:
            token_id: Comma-separated Token IDs
            symbol: Comma-separated Token Symbols
            limit: Number of records to return
            page: Page number for pagination
            
        Returns:
            str: A formatted string containing the resistance and support analysis
        """
        try:
            if not token_id and not symbol:
                return "Error: Please provide either token_id or symbol"
                
            params = {
                'token_id': token_id,
                'symbol': symbol,
                'limit': limit,
                'page': page
            }
            
            # Remove None values
            params = {k: v for k, v in params.items() if v is not None}
            
            response = self.client.base_endpoint._request("get", "/resistance-support", params=params)
            
            # Format the response as a readable string
            if isinstance(response, dict) and 'data' in response:
                levels_data = response['data']
                if not levels_data:
                    return "No resistance and support levels found for the specified criteria."
                
                result = []
                for entry in levels_data:
                    token_info = [
                        f"Token ID: {entry.get('TOKEN_ID', 0)}",
                        f"Token Name: {entry.get('TOKEN_NAME', '')}",
                        f"Token Symbol: {entry.get('TOKEN_SYMBOL', '')}",
                        f"Analysis Date: {entry.get('DATE', '')}",
                        "\nKey Price Levels:"
                    ]
                    
                    # Add historical levels if available
                    historical_levels = entry.get('HISTORICAL_RESISTANCE_SUPPORT_LEVELS', [])
                    if historical_levels:
                        # Sort levels by price, descending
                        historical_levels.sort(key=lambda x: float(x.get('level', 0)), reverse=True)
                        
                        # Add historical levels
                        token_info.append("\nHistorical Levels:")
                        for level in historical_levels:
                            price = float(level.get('level', 0))
                            date = level.get('date', '')
                            token_info.append(
                                f"  ${price:,.2f} (Date: {date})"
                            )
                    else:
                        token_info.append("No historical levels available")
                    
                    # Add market context if available
                    market_context = entry.get('market_context', {})
                    if market_context:
                        token_info.extend([
                            "\nMarket Context:",
                            f"Trend Direction: {market_context.get('trend_direction', '')}",
                            f"Volume Profile: {market_context.get('volume_profile', '')}",
                            f"Price Action: {market_context.get('price_action', '')}",
                            f"Volatility: {market_context.get('volatility', '')}"
                        ])
                    
                    result.append("\n".join(token_info))                 
            
            return str(response)
            
        except Exception as e:
            return self._handle_error(e)
    
    def _arun(self, **kwargs) -> str:
        """Async implementation of the tool (not implemented)."""
        raise NotImplementedError("Async version not implemented") 