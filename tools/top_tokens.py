from typing import Optional
from pydantic import Field, field_validator, ValidationInfo
from datetime import datetime

from .base_tool import TMBaseTool, TMBaseToolInput

class TopTokensToolInput(TMBaseToolInput):
    """Input schema for the Top Tokens tool."""
    top_k: Optional[int] = Field(
        100,
        description="Number of top tokens to retrieve"
    )

class TopTokensTool(TMBaseTool):
    """Tool for accessing top tokens by various ranking criteria."""
    
    name: str = "get_top_tokens"
    description: str = """Get and analyze top cryptocurrency tokens ranked by market capitalization.
    Useful when you need to:
    - Find top tokens by market cap
    - Track highest volume tokens
    - Monitor best performing tokens
    - Analyze token holder distribution
    - Track social media popularity
    - Compare tokens across categories
    
    The tool provides detailed information including:
    - Market capitalization
    - Trading volume
    - Price changes
    - Holder statistics
    - Social metrics
    - Token rankings
    
    You can specify:
    - top_k: Number of top tokens to retrieve (by market cap)
    """
    args_schema = TopTokensToolInput

    def _run(
        self,        
        top_k: Optional[int] = 100, 
    ) -> str:
        """Run the tool to get top tokens data.
        
        Args:
            top_k: Number of top tokens to retrieve
            
        Returns:
            str: A formatted string containing the top tokens data
        """
        try:                         
            if top_k <= 0:
                return "Error: top_k must be positive"
                       
            params = {                
                'top_k': top_k,                
            }
            
            # Remove None values
            params = {k: v for k, v in params.items() if v is not None}
            
            response = self.client.base_endpoint._request("get", "/top-market-cap-tokens", params=params)
            
            # Format the response as a readable string
            if isinstance(response, dict) and 'data' in response:
                data = response['data']
                if not data:
                    return "No market metrics data found for the specified criteria."
                
                # Format the response to match the example schema
                formatted_response = {
                    "success": True,
                    "message": "Data fetched successfully",
                    "length": len(data),
                    "data": []
                }
                
                # Process each token and add to the formatted response
                for token in data:
                    formatted_token = {
                        "TOKEN_ID": token.get('TOKEN_ID', 0),
                        "TOKEN_NAME": token.get('TOKEN_NAME', 'Unknown'),
                        "TOKEN_SYMBOL": token.get('TOKEN_SYMBOL', 'Unknown'),
                        "EXCHANGE_LIST": token.get('EXCHANGE_LIST', []),
                        "CATEGORY_LIST": token.get('CATEGORY_LIST', [])
                    }
                    formatted_response["data"].append(formatted_token)
                
                return formatted_response
            
            return str(response)
        except Exception as e:
            return self._handle_error(e)
    
    def _arun(self, **kwargs) -> str:
        """Async implementation of the tool (not implemented)."""
        raise NotImplementedError("Async version not implemented") 