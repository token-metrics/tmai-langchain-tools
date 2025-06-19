from typing import Optional
from pydantic import Field, field_validator, ValidationInfo
from datetime import datetime

from .base_tool import TMBaseTool, TMBaseToolInput

class SectorIndicesHoldingsToolInput(TMBaseToolInput):
    """Input schema for the Sector Indices Holdings tool."""
    id: Optional[str] = Field(
        None,
        description="Id of the index. Example 1"
    )
  
class SectorIndicesHoldingsTool(TMBaseTool):
    """Tool for analyzing sector indices holdings and composition."""
    
    name:str = "analyze_sector_indices_holdings"
    description:str = """Analyze the composition and holdings of sector-specific cryptocurrency indices.
    Useful when you need to:
    - Track index composition
    - Monitor token weights
    - Analyze sector exposure
    - Study market cap distribution
    - Track volume distribution
    - Evaluate sector representation
    
    The tool provides detailed holdings data including:
    - Token weights
    - Market capitalization
    - Trading volumes
    - Composition changes
    - Sector allocation
    - Historical snapshots
    
    You can analyze:
    - Specific sector indices
    - Time periods
    - Token weights
    - Market cap distribution
    - Volume patterns
    - Sector exposure
    
    """
    args_schema = SectorIndicesHoldingsToolInput

    def _run(
        self,
        id: str,      
    ) -> str:
        """Run the tool to analyze sector indices holdings.
        
        Args:
            id: Id of the index. Example 1
            
        Returns:
            str: A formatted string containing the holdings analysis
        """
        try:
            params = {
                'id': id,                
            }
            
            # Remove None values
            params = {k: v for k, v in params.items() if v is not None}
            
            response = self.client.base_endpoint._request("get", "/indices-holdings", params=params)
            
            # Format the response as a readable string
            if isinstance(response, dict) and 'data' in response:
                holdings = response['data']
                if not holdings:
                    return "No holdings data found for the specified criteria."
                
                # Group tokens by date to organize them properly
                holdings_by_date = {}
                for token in holdings:
                    date = token.get('DATE', 'Unknown')
                    if date not in holdings_by_date:
                        holdings_by_date[date] = []
                    holdings_by_date[date].append(token)
                
                result = []
                for date, tokens in holdings_by_date.items():
                    # Sort tokens by weight for better presentation
                    tokens.sort(key=lambda x: float(x.get('WEIGHT', 0)), reverse=True)                                                            
                    
                    analysis = [
                        f"Date: {date}",
                        "\nHoldings Breakdown:"
                    ]
                    
                    total_weight = sum(float(token.get('WEIGHT', 0)) for token in tokens)
                    analysis.append(f"Total Weight Represented: {total_weight:.2f}%")
                    
                    for token in tokens:
                        token_details = [
                            f"  {token.get('TOKEN_NAME', 'Unknown')} ({token.get('TOKEN_SYMBOL', 'Unknown')})",
                            f"    ID: {token.get('TOKEN_ID', 0)}",
                            f"    Weight: {float(token.get('WEIGHT', 0)):.2f}%",
                            f"    Market Cap: ${float(token.get('MARKET_CAP', 0)):,.2f}",
                            f"    Price: ${float(token.get('PRICE', 0)):,.2f}",
                            f"    Current ROI: {float(token.get('CURRENT_ROI', 0)):.2f}%",
                            f"    Trader Grade: {float(token.get('TRADER_GRADE', 0)):.2f}",
                            f"    24h Grade Change: {float(token.get('TRADER_GRADE_CHANGE_24H', 0)):.2f}"
                        ]
                        analysis.extend(token_details)
                    
                    result.append("\n".join(analysis))
                
                pagination = response.get('pagination', {})
                total_tokens = pagination.get('total', 0)
                
                summary = [
                    f"\nSummary:",
                    f"Total Tokens: {total_tokens}"
                ]
                
                return "\n\n" + "\n\n---\n\n".join(result) + "\n\n" + "\n".join(summary)
            
            return str(response)
            
        except Exception as e:
            return self._handle_error(e)
    
    def _arun(self, **kwargs) -> str:
        """Async implementation of the tool (not implemented)."""
        raise NotImplementedError("Async version not implemented") 