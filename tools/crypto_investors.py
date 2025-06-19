from typing import Optional
from pydantic import Field, field_validator
from datetime import datetime

from .base_tool import TMBaseTool, TMBaseToolInput

class CryptoInvestorsToolInput(TMBaseToolInput):
    """Input schema for the Crypto Investors tool."""
    limit: Optional[int] = Field(
        50,
        description="Number of records to return per page"
    )
    page: Optional[int] = Field(
        1,
        description="Page number for pagination"
    )


class CryptoInvestorsTool(TMBaseTool):
    """Tool for accessing crypto institutional investor data and analytics."""
    
    name: str = "analyze_crypto_investors"
    description: str = """Analyze institutional and major crypto investors' data and investment patterns.
    Useful when you need to:
    - Track major investors' activities
    - Analyze investment patterns
    - Monitor portfolio performance
    - Study investment strategies
    - Track regional investment flows
    - Evaluate investor success rates
    
    The tool provides detailed information including:
    - Investor profiles and types
    - Portfolio compositions
    - Investment history
    - Performance metrics
    - Regional distribution
    - Investment patterns
    
    You can control the output with:
    - limit: Number of investor records to return
    - page: Page number for pagination
    """
    args_schema = CryptoInvestorsToolInput

    def _run(
        self,
        limit: Optional[int] = 50,
        page: Optional[int] = 1
    ) -> str:
        """Run the tool to get crypto investor data.
        
        Args:
            limit: Number of records to return
            page: Page number for pagination
            
        Returns:
            str: A formatted string containing the crypto investor data
        """
        try:           
            
            params = {                
                'limit': limit,
                'page': page
            }
            
            # Remove None values
            params = {k: v for k, v in params.items() if v is not None}
            
            response = self.client.base_endpoint._request("get", "/crypto-investors", params=params)
            
            # Format the response as a readable string
            if isinstance(response, dict) and 'data' in response:
                data = response['data']
                if not data:
                    return "No market metrics data found for the specified criteria."
                
                result = []
                for investor in data:
                    analysis = [
                        f"Investor Name: {investor.get('INVESTOR_NAME', 'Unknown')}",
                        f"Website: {investor.get('INVESTOR_WEBSITE', 'Unknown')}",
                        f"Twitter: {investor.get('INVESTOR_TWITTER', 'Unknown')}",
                        f"Number of Investments: {investor.get('ROUND_COUNT', 'Unknown')}",
                        f"Average ROI: {investor.get('ROI_AVERAGE', 0)}",
                        f"Median ROI: {investor.get('ROI_MEDIAN', 0)}"
                    ]
                    result.append("\n".join(analysis))
                
                return "\n\n" + "\n\n---\n\n".join(result)
            
            return str(response)
            
        except Exception as e:
            return self._handle_error(e)
    
    def _arun(self, **kwargs) -> str:
        """Async implementation of the tool (not implemented)."""
        raise NotImplementedError("Async version not implemented") 