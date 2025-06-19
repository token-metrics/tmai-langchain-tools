import os
import sys 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_endpoint import BaseEndpoint

class TokensEndpoint(BaseEndpoint):
    """Endpoint for accessing token information"""
    
    def get(self, token_id=None, token_name=None, symbol=None, category=None, 
            exchange=None, blockchain_address=None, limit=50, page=1):
        """Get the list of tokens supported by Token Metrics.
        
        This endpoint provides access to information about all crypto assets including
        TOKEN_ID, TOKEN_NAME, TOKEN_SYMBOL, EXCHANGE_LIST, CATEGORY_LIST, 
        CONTRACT_ADDRESS, and TM_LINK.
        
        Args:
            token_id (str, optional): Comma-separated Token IDs (e.g., "3375" for BTC)
            token_name (str, optional): Comma-separated Token Names (e.g., "Bitcoin, Ethereum")
            symbol (str, optional): Comma-separated Token Symbols (e.g., "BTC,ETH")
            category (str, optional): Comma-separated category names (e.g., "layer-1,nft")
            exchange (str, optional): Comma-separated exchange names (e.g., "binance,gate")
            blockchain_address (str, optional): Blockchain name and contract address (e.g., "binance-smart-chain:0x57185189118c7e786cafd5c71f35b16012fa95ad")
            limit (int, optional): Limit the number of items in response
            page (int, optional): Page number for pagination
            
        Returns:
            dict: Token information including:
                - TOKEN_ID: Token ID for identifying each cryptocurrency
                - TOKEN_NAME: The name of the crypto asset
                - TOKEN_SYMBOL: The symbol of the crypto asset
                - EXCHANGE_LIST: Exchanges where token is listed
                - CATEGORY_LIST: Categories the token belongs to
                - CONTRACT_ADDRESS: Contract address on all available chains
                - TM_LINK: Direct link to Token Metrics token details page
        """
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
        
        return self._request('get', 'tokens', params)
    
    def get_dataframe(self, **kwargs):
        """Get token information as a pandas DataFrame.
        
        Args:
            **kwargs: Arguments to pass to the get method
            
        Returns:
            pandas.DataFrame: DataFrame containing token information
        """
        data = self.get(**kwargs)
        return self.to_dataframe(data)    
