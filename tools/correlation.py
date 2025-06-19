from typing import Optional
from pydantic import Field, field_validator, ValidationInfo
from datetime import datetime

from .base_tool import TMBaseTool, TMBaseToolInput

class CorrelationToolInput(TMBaseToolInput):
    """Input schema for the Correlation Analysis tool."""
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
    limit: Optional[int] = Field(
        50,
        description="Number of records to return per page"
    )
    page: Optional[int] = Field(
        1,
        description="Page number for pagination"
    )


class CorrelationTool(TMBaseTool):
    """Tool for analyzing correlations between cryptocurrencies."""
    
    name: str = "analyze_correlations"
    description: str = """Analyze price correlations between different cryptocurrencies.
    Useful when you need to:
    - Study relationships between tokens
    - Build diversified portfolios
    - Identify market patterns
    - Analyze market segments
    - Track correlation changes
    - Find uncorrelated assets
    
    The tool provides detailed correlation data including:
    - Correlation coefficients
    - Time period analysis
    - Statistical confidence
    - Sample size information
    - Historical trends
    - Market segment patterns
    
    You can analyze:
    - Specific token pairs (using token_id or symbol)
    - Market segments (using category)
    - Exchange-specific correlations (using exchange)
    - Correlation strength
    - Statistical significance
    - Historical patterns
    """
    args_schema = CorrelationToolInput

    def _run(
        self,
        token_id: Optional[str] = None,
        symbol: Optional[str] = None,
        category: Optional[str] = None,
        exchange: Optional[str] = None,
        limit: Optional[int] = 50,
        page: Optional[int] = 1
    ) -> str:
        """Run the tool to analyze correlations between cryptocurrencies.
        
        Args:
            token_id: Comma separated token IDs
            symbol: Comma separated token symbols
            category: Filter by token category
            exchange: Filter by exchange listing
            limit: Number of records per page
            page: Page number
            
        Returns:
            str: A formatted string containing the correlation analysis
        """
        try:
            params = {
                'token_id': token_id,
                'symbol': symbol,
                'category': category,
                'exchange': exchange,
                'limit': limit,
                'page': page
            }
            
            # Remove None values
            params = {k: v for k, v in params.items() if v is not None}
            
            response = self.client.base_endpoint._request("get", "/correlation", params=params)
            
            # Format the response as a readable string
            if isinstance(response, dict) and 'data' in response:
                correlations = response['data']
                if not correlations:
                    return "No correlation data found for the specified criteria."
                
                result = []
                for corr in correlations:
                    analysis = [
                        f"Token ID: {corr.get('TOKEN_ID', 0)}",
                        f"Token Name: {corr.get('TOKEN_NAME', 'Unknown')}",
                        f"Token Symbol: {corr.get('TOKEN_SYMBOL', 'Unknown')}",
                        f"Date: {corr.get('DATE', 'Unknown')}",
                        "\nTop Correlations:"
                    ]
                    
                    # Add top correlations
                    top_correlations = corr.get('TOP_CORRELATION', [])
                    for corr_data in top_correlations:
                        correlation_value = corr_data.get('correlation', 0)
                        # Format correlation with appropriate sign
                        if correlation_value > 0:
                            correlation_str = f"+{correlation_value:.4f}"
                        else:
                            correlation_str = f"{correlation_value:.4f}"
                        
                        analysis.append(
                            f"- {corr_data.get('token', 'Unknown')}: {correlation_str}"
                        )
                    
                    result.append("\n".join(analysis))
                
                return "\n\n" + "\n\n---\n\n".join(result)
            
            return str(response)
            
        except Exception as e:
            return self._handle_error(e)
    
    def _arun(self, **kwargs) -> str:
        """Async implementation of the tool (not implemented)."""
        raise NotImplementedError("Async version not implemented") 