from typing import Optional
from pydantic import Field, field_validator, ValidationInfo
from datetime import datetime

from .base_tool import TMBaseTool, TMBaseToolInput

class QuantmetricsToolInput(TMBaseToolInput):
    """Input schema for the Quantitative Metrics tool."""
    token_id: Optional[str] = Field(
        None,
        description="Comma separated token IDs to analyze"
    )
    symbol: Optional[str] = Field(
        None,
        description="Comma separated token symbols to analyze"
    )
    category: Optional[str] = Field(
        None,
        description="Filter by token category (e.g., 'layer-1', 'nft')"
    )
    exchange: Optional[str] = Field(
        None,
        description="Filter by exchange listing (e.g., 'binance', 'gate')"
    )
    marketcap: Optional[float] = Field(
        None,
        description="Minimum market capitalization in USD"
    )
    volume: Optional[float] = Field(
        None,
        description="Minimum 24h trading volume in USD"
    )
    fdv: Optional[float] = Field(
        None,
        description="Minimum fully diluted valuation in USD"
    )
    
    limit: Optional[int] = Field(
        50,
        description="Number of records to return per page"
    )
    page: Optional[int] = Field(
        1,
        description="Page number for pagination"
    )

class QuantmetricsTool(TMBaseTool):
    """Tool for accessing advanced quantitative metrics and analytics."""
    
    name: str = "analyze_quant_metrics"
    description: str = """Analyze comprehensive quantitative metrics for cryptocurrencies.
    Useful when you need to:
    - Evaluate token volatility
    - Assess market liquidity
    - Analyze momentum indicators
    - Study valuation metrics
    - Compare tokens quantitatively
    - Track market efficiency
    
    The tool provides detailed metrics including:
    - Volatility metrics (daily, weekly, monthly)
    - Liquidity analysis (bid-ask spread, depth)
    - Momentum indicators (RSI, MACD)
    - Valuation metrics (P/E ratio, Market/TVL)
    - Market efficiency metrics
    
    You can filter by:
    - Specific tokens (token_id or symbol)
    - Token categories
    - Exchanges
    - Market cap thresholds (marketcap)
    - Volume requirements (volume)
    - Fully diluted valuation (fdv)
    """
    args_schema = QuantmetricsToolInput

    def _run(
        self,
        token_id: Optional[str] = None,
        symbol: Optional[str] = None,
        category: Optional[str] = None,
        exchange: Optional[str] = None,
        marketcap: Optional[float] = None,
        volume: Optional[float] = None,
        fdv: Optional[float] = None,
        limit: Optional[int] = 50,
        page: Optional[int] = 1
    ) -> str:
        """Run the tool to get quantitative metrics.
        
        Args:
            token_id: Comma separated token IDs
            symbol: Comma separated token symbols
            category: Filter by token category
            exchange: Filter by exchange listing
            marketcap: Minimum market capitalization
            volume: Minimum 24h trading volume
            fdv: Minimum fully diluted valuation
            limit: Number of records to return
            page: Page number for pagination
            
        Returns:
            str: A formatted string containing the quantitative metrics
        """
        try:                     
            params = {
                'token_id': token_id,
                'symbol': symbol,
                'category': category,
                'exchange': exchange,
                'marketcap': marketcap,
                'volume': volume,
                'fdv': fdv,
                'limit': limit,
                'page': page
            }
            
            # Remove None values
            params = {k: v for k, v in params.items() if v is not None}
            
            response = self.client.base_endpoint._request("get", "/quantmetrics", params=params)
            
            # Format the response as a readable string
            if isinstance(response, dict) and 'data' in response:
                metrics = response['data']
                if not metrics:
                    return "No quantitative metrics found for the specified criteria."
                
                result = []
                for metric in metrics:
                    analysis = [
                        f"Token: {metric.get('TOKEN_NAME', 'Unknown')} ({metric.get('TOKEN_SYMBOL', 'Unknown')})",
                        f"ID: {metric.get('TOKEN_ID', 0)}",
                        f"Date: {metric.get('DATE', 'Unknown')}",
                        "\nQuantitative Metrics:",
                        f"- Volatility: {float(metric.get('VOLATILITY', 0)):,.2f}",
                        f"- All Time Return: {float(metric.get('ALL_TIME_RETURN', 0)):,.2f}%",
                        f"- CAGR: {float(metric.get('CAGR', 0)):,.2f}%",
                        f"- Sharpe Ratio: {float(metric.get('SHARPE', 0)):,.2f}",
                        f"- Sortino Ratio: {float(metric.get('SORTINO', 0)):,.2f}",
                        f"- Maximum Drawdown: {float(metric.get('MAX_DRAWDOWN', 0)):,.2f}%",
                        f"- Skew: {float(metric.get('SKEW', 0)):,.2f}",
                        f"- Tail Ratio: {float(metric.get('TAIL_RATIO', 0)):,.2f}",
                        f"- Risk/Reward Ratio: {float(metric.get('RISK_REWARD_RATIO', 0)):,.2f}",
                        f"- Profit Factor: {float(metric.get('PROFIT_FACTOR', 0)):,.2f}",
                        f"- Kurtosis: {float(metric.get('KURTOSIS', 0)):,.2f}",
                        f"- Daily Value at Risk: {float(metric.get('DAILY_VALUE_AT_RISK', 0)):,.2f}%",
                        f"- Daily Return Average: {float(metric.get('DAILY_RETURN_AVG', 0)):,.6f}%",
                        f"- Daily Return Std Dev: {float(metric.get('DAILY_RETURN_STD', 0)):,.6f}%"
                    ]
                    result.append("\n".join(analysis))
                
                return "\n\n" + "\n\n---\n\n".join(result)
            
            return str(response)
            
        except Exception as e:
            return self._handle_error(e)
    
    def _arun(self, **kwargs) -> str:
        """Async implementation of the tool (not implemented)."""
        raise NotImplementedError("Async version not implemented") 