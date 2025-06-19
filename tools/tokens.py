import os
import sys 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.base_tool import TMBaseTool, TMBaseToolInput
from typing import Optional
from pydantic import Field



class TokensToolInput(TMBaseToolInput):
    """Input schema for the Tokens tool."""
    token_id: Optional[str] = Field(
        None,
        description="Comma-separated Token IDs (e.g., '3375' for BTC)"
    )
    token_name: Optional[str] = Field(
        None,
        description="Comma-separated Token Names (e.g., 'Bitcoin, Ethereum')"
    )
    symbol: Optional[str] = Field(
        None,
        description="Comma-separated Token Symbols (e.g., 'BTC,ETH')"
    )
    category: Optional[str] = Field(
        None,
        description="Comma-separated category names (e.g., 'layer-1,nft')"
    )
    exchange: Optional[str] = Field(
        None,
        description="Comma-separated exchange names (e.g., 'binance,gate')"
    )
    blockchain_address: Optional[str] = Field(
        None,
        description="Blockchain name and contract address (e.g., 'binance-smart-chain:0x57185189118c7e786cafd5c71f35b16012fa95ad')"
    )
    limit: Optional[int] = Field(
        1000,
        description="Limit the number of items in response"
    )
    page: Optional[int] = Field(
        1,
        description="Page number for pagination"
    )

class TokensTool(TMBaseTool):
    """Tool for accessing token information from Token Metrics."""
    
    name: str = "get_token_info"
    description: str = """Get information about cryptocurrencies including their IDs, names, symbols, exchanges, categories, and contract addresses.
    Useful when you need to:
    - Look up basic information about cryptocurrencies
    - Find tokens by name, symbol, or ID
    - Get contract addresses for tokens
    - See which exchanges list particular tokens
    - Find tokens in specific categories
    
    You can filter by:
    - token_id: Comma-separated Token IDs (e.g., "3375" for BTC)
    - token_name: Comma-separated Token Names (e.g., "Bitcoin, Ethereum")
    - symbol: Comma-separated Token Symbols (e.g., "BTC,ETH")
    - category: Comma-separated category names (e.g., "layer-1,nft")
    - exchange: Comma-separated exchange names (e.g., "binance,gate")
    - blockchain_address: Blockchain name and contract address
    """
    args_schema = TokensToolInput
    def _run(
        self,
        token_id: Optional[str] = None,
        token_name: Optional[str] = None,
        symbol: Optional[str] = None,
        category: Optional[str] = None,
        exchange: Optional[str] = None,
        blockchain_address: Optional[str] = None,
        limit: Optional[int] = 1000,
        page: Optional[int] = 1
    ) -> str:
        """Run the tool to get token information.
        
        Args:
            token_id: Comma-separated Token IDs (e.g., "3375" for BTC)
            token_name: Comma-separated Token Names (e.g., "Bitcoin, Ethereum")
            symbol: Comma-separated Token Symbols (e.g., "BTC,ETH")
            category: Comma-separated category names (e.g., "layer-1,nft")
            exchange: Comma-separated exchange names (e.g., "binance,gate")
            blockchain_address: Blockchain name and contract address
            limit: Limit the number of items in response
            page: Page number for pagination
            
        Returns:
            str: A formatted string containing the token information
        """
        try:
            # Build the parameters dictionary
            params = {
                'token_id': token_id,
                'token_name': token_name,
                'symbol': symbol,
                'category': category,
                'exchange': exchange,
                'blockchain_address': blockchain_address,
                'limit': limit,
                'page': page
            }
            
            # Remove None values
            params = {k: v for k, v in params.items() if v is not None}
            
            # Make the API request
            response = self.client.base_endpoint._request("get", "/tokens", params=params)
            # data = response.json()
            
            # Format the response as a readable string
            if isinstance(response, dict) and 'data' in response:
                tokens = response['data']
                if not tokens:
                    return "No tokens found matching the specified criteria."
                
                result = []
                # print(tokens)
                for token in tokens:                    
                    token_info = [
                        f"Name: {token.get('TOKEN_NAME', 'Unknown')}",
                        f"Symbol: {token.get('TOKEN_SYMBOL', 'Unknown')}",
                        f"Token ID: {token.get('TOKEN_ID', 'Unknown')}",
                        f"Categories: {', '.join([cat['category_name'] for cat in token.get('CATEGORY_LIST', [])])}",
                        f"Exchanges: {', '.join([ex['exchange_name'] for ex in token.get('EXCHANGE_LIST', [])])}",
                        f"Contract Addresses: {', '.join([f'{chain}: {addr}' for chain, addr in token.get('CONTRACT_ADDRESS', {}).items()])}"
                    ]
                    result.append("\n".join(token_info))
                
                return "\n\n".join(result)
            
            return str(response)
            
        except Exception as e:
            return self._handle_error(e)
    
    def _arun(self, **kwargs) -> str:
        """Async implementation of the tool (not implemented)."""
        raise NotImplementedError("Async version not implemented")
