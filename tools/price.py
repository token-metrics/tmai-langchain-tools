from typing import Optional
from pydantic import Field

from .base_tool import TMBaseTool, TMBaseToolInput

class PriceToolInput(TMBaseToolInput):
    """Input schema for the Price tool."""
    token_id: Optional[str] = Field(
        None,
        description="Comma-separated Token IDs (e.g., '3375' for BTC)"
    )

class PriceTool(TMBaseTool):
    """Tool for accessing current price data for cryptocurrencies."""
    
    name: str = "get_crypto_price"
    description: str = """Get current price data for cryptocurrencies.
    Useful when you need to know the current price of one or more cryptocurrencies.
    You should provide token IDs as a comma-separated string (e.g., "3375" for BTC).
    """
    args_schema = PriceToolInput

    def _run(self, token_id: Optional[str] = None) -> str:
        """Run the tool to get current price data.
        
        Args:
            token_id: Comma-separated Token IDs (e.g., "3375" for BTC)
            
        Returns:
            str: A formatted string containing the price data
        """
        try:
            params = {'token_id': token_id} if token_id else {}
            response = self.client.base_endpoint._request("get", "/price", params=params)
            
            # Format the response as a readable string
            if isinstance(response, dict) and 'data' in response:
                data = response['data']
                if not data:
                    return "No price data found for the specified tokens."
                
                result = []
                for price in data:
                    token_id = price.get('TOKEN_ID', 'Unknown')
                    token_name = price.get('TOKEN_NAME', 'Unknown')
                    current_price = price.get('CURRENT_PRICE', 'Unknown')
                    token_symbol = price.get('TOKEN_SYMBOL', 'Unknown')
                    result.append(f"Token ID: {token_id} || Token Name: {token_name} || Token Symbol: {token_symbol} || Current Price: ${current_price}")
                
                return "\n".join(result)
            
            return str(response)
            
        except Exception as e:
            return self._handle_error(e)
    
    def _arun(self, token_id: Optional[str] = None) -> str:
        """Async implementation of the tool (not implemented)."""
        raise NotImplementedError("Async version not implemented") 