from typing import Optional
from pydantic import Field, field_validator
from datetime import datetime

from .base_tool import TMBaseTool, TMBaseToolInput

class TraderIndicesToolInput(TMBaseToolInput):
    """Input schema for the Trader Indices tool."""
    index_type: Optional[str] = Field(
        None,
        description="Type of trading index ('momentum', 'value', 'growth', 'quality', 'multi_factor')"
    )
    strategy: Optional[str] = Field(
        None,
        description="Trading strategy focus ('long_only', 'long_short', 'market_neutral', 'arbitrage')"
    )
    risk_profile: Optional[str] = Field(
        None,
        description="Risk tolerance level ('conservative', 'moderate', 'aggressive')"
    )
    token_id: Optional[str] = Field(
        None,
        description="Comma separated token IDs to include"
    )
    symbol: Optional[str] = Field(
        None,
        description="Comma separated token symbols to include"
    )
    min_aum: Optional[float] = Field(
        None,
        description="Minimum assets under management in USD"
    )
    min_return: Optional[float] = Field(
        None,
        description="Minimum historical return percentage"
    )
    rebalance_frequency: Optional[str] = Field(
        None,
        description="Portfolio rebalancing frequency ('daily', 'weekly', 'monthly')"
    )
    start_date: Optional[str] = Field(
        None,
        description="Start date in YYYY-MM-DD format"
    )
    end_date: Optional[str] = Field(
        None,
        description="End date in YYYY-MM-DD format"
    )
    limit: Optional[int] = Field(
        1000,
        description="Number of records to return per page"
    )
    page: Optional[int] = Field(
        1,
        description="Page number for pagination"
    )

    @field_validator('min_aum')
    @classmethod
    def validate_min_aum(cls, v):
        if v is not None and v < 0:
            raise ValueError("min_aum must be non-negative")
        return v

    @field_validator('min_return')
    @classmethod
    def validate_min_return(cls, v):
        if v is not None and v < -100:
            raise ValueError("min_return must be greater than -100%")
        return v

class TraderIndicesTool(TMBaseTool):
    """Tool for analyzing trading indices."""
    
    name: str = "analyze_trading_indices"
    description: str = """Analyze AI-generated trading portfolios and their performance metrics.
    Useful when you need to:
    - Evaluate different trading strategies
    - Analyze portfolio performance
    - Monitor risk metrics
    - Track trading success rates
    - Review portfolio compositions
    - Check rebalancing schedules
    
    The tool provides comprehensive analysis including:
    - Portfolio composition and weights
    - Performance metrics (returns, risk-adjusted returns)
    - Risk metrics (volatility, drawdown, VaR)
    - Trading metrics (win rate, profit factor)
    - Rebalancing information
    
    You can filter by:
    - Index type (momentum, value, growth, etc.)
    - Trading strategy (long_only, long_short, etc.)
    - Risk profile
    - Specific tokens
    - Minimum AUM or returns
    - Rebalancing frequency
    - Date range
    """
    args_schema = TraderIndicesToolInput

    def _run(
        self,
        index_type: Optional[str] = None,
        strategy: Optional[str] = None,
        risk_profile: Optional[str] = None,
        token_id: Optional[str] = None,
        symbol: Optional[str] = None,
        min_aum: Optional[float] = None,
        min_return: Optional[float] = None,
        rebalance_frequency: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: Optional[int] = 1000,
        page: Optional[int] = 1
    ) -> str:
        """Run the tool to get trader indices data.
        
        Args:
            index_type: Type of trading index
            strategy: Trading strategy focus
            risk_profile: Risk tolerance level
            token_id: Comma separated token IDs
            symbol: Comma separated token symbols
            min_aum: Minimum assets under management
            min_return: Minimum historical return
            rebalance_frequency: Portfolio rebalancing frequency
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            limit: Number of records to return
            page: Page number for pagination
            
        Returns:
            str: A formatted string containing the trader indices data
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
            
            # Validate index_type if provided
            valid_index_types = ['momentum', 'value', 'growth', 'quality', 'multi_factor']
            if index_type and index_type not in valid_index_types:
                return f"Error: index_type must be one of {', '.join(valid_index_types)}"
            
            # Validate strategy if provided
            valid_strategies = ['long_only', 'long_short', 'market_neutral', 'arbitrage']
            if strategy and strategy not in valid_strategies:
                return f"Error: strategy must be one of {', '.join(valid_strategies)}"
            
            # Validate risk_profile if provided
            valid_risk_profiles = ['conservative', 'moderate', 'aggressive']
            if risk_profile and risk_profile not in valid_risk_profiles:
                return f"Error: risk_profile must be one of {', '.join(valid_risk_profiles)}"
            
            # Validate rebalance_frequency if provided
            valid_frequencies = ['daily', 'weekly', 'monthly']
            if rebalance_frequency and rebalance_frequency not in valid_frequencies:
                return f"Error: rebalance_frequency must be one of {', '.join(valid_frequencies)}"
            
            # Validate numeric inputs
            if min_aum is not None and min_aum < 0:
                return "Error: min_aum must be non-negative"
            
            if min_return is not None and min_return < -100:
                return "Error: min_return must be greater than -100%"
            
            params = {
                'index_type': index_type,
                'strategy': strategy,
                'risk_profile': risk_profile,
                'token_id': token_id,
                'symbol': symbol,
                'min_aum': min_aum,
                'min_return': min_return,
                'rebalance_frequency': rebalance_frequency,
                'start_date': start_date,
                'end_date': end_date,
                'limit': limit,
                'page': page
            }
            
            # Remove None values
            params = {k: v for k, v in params.items() if v is not None}
            
            data = self.client.trader_indices.get(**params)
            
            # Format the response as a readable string
            if isinstance(data, dict) and 'data' in data:
                indices = data['data']
                if not indices:
                    return "No trading indices found for the specified criteria."
                
                result = []
                for index in indices:
                    index_info = index.get('index_info', {})
                    portfolio = index.get('portfolio_composition', {})
                    performance = index.get('performance_metrics', {})
                    rebalancing = index.get('rebalancing_info', {})
                    
                    returns = performance.get('returns', {})
                    risk = performance.get('risk_metrics', {})
                    trading = performance.get('trading_metrics', {})
                    
                    analysis = [
                        f"Index: {index_info.get('name', 'Unknown')}",
                        f"Type: {index_info.get('type', 'Unknown')}",
                        f"Strategy: {index_info.get('strategy', 'Unknown')}",
                        f"Risk Profile: {index_info.get('risk_profile', 'Unknown')}",
                        "\nPortfolio Composition:",
                        f"- Holdings: {portfolio.get('holdings', 'Unknown')}",
                        f"- Weights: {portfolio.get('weights', 'Unknown')}",
                        f"- Sector Exposure: {portfolio.get('sector_exposure', 'Unknown')}",
                        f"- Risk Exposure: {portfolio.get('risk_exposure', 'Unknown')}",
                        "\nPerformance Metrics:",
                        f"- Total Return: {returns.get('total_return', 'Unknown')}",
                        f"- Period Returns: {returns.get('period_returns', 'Unknown')}",
                        f"- Risk-Adjusted Return: {returns.get('risk_adjusted_return', 'Unknown')}",
                        "\nRisk Metrics:",
                        f"- Volatility: {risk.get('volatility', 'Unknown')}",
                        f"- Drawdown: {risk.get('drawdown', 'Unknown')}",
                        f"- VaR: {risk.get('var', 'Unknown')}",
                        "\nTrading Metrics:",
                        f"- Win Rate: {trading.get('win_rate', 'Unknown')}",
                        f"- Profit Factor: {trading.get('profit_factor', 'Unknown')}",
                        f"- Recovery Factor: {trading.get('recovery_factor', 'Unknown')}",
                        "\nRebalancing Information:",
                        f"- Last Rebalance: {rebalancing.get('last_rebalance', 'Unknown')}",
                        f"- Next Rebalance: {rebalancing.get('next_rebalance', 'Unknown')}"
                    ]
                    result.append("\n".join(analysis))
                
                return "\n\n" + "\n\n---\n\n".join(result)
            
            return str(data)
            
        except Exception as e:
            return self._handle_error(e)
    
    def _arun(self, **kwargs) -> str:
        """Async implementation of the tool (not implemented)."""
        raise NotImplementedError("Async version not implemented")
