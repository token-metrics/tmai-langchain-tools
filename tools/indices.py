from typing import Optional
from pydantic import Field
from datetime import datetime

from .base_tool import TMBaseTool, TMBaseToolInput

class IndicesToolInput(TMBaseToolInput):
    """Input schema for the Indices tool."""
    indicesType: Optional[str] = Field(
        None,
        description="Filter to return indices by type: 'active' for actively managed, 'passive' for passively managed."
    )
    limit: Optional[int] = Field(
        50,
        description="Number of records to return per page"
    )
    page: Optional[int] = Field(
        1,
        description="Page number for pagination"
    )


class IndicesTool(TMBaseTool):
    """Tool for retrieving cryptocurrency indices information."""
    
    name: str = "get_indices"
    description: str = """Get the list of cryptocurrency indices and their performance metrics.
    Useful when you need to:
    - View available cryptocurrency indices
    - Track index performance
    - Monitor market trends
    - Compare different indices
    - Analyze sector performance
    
    The tool provides detailed indices metrics including:
    - Index ID and name
    - Current price
    - Number of coins in the index
    - Performance metrics (24h, 7d, 1m)
    - Trading volume
    - Market capitalization
    - Index grade
    - All-time performance
    - Top gainers in each index
    
    You can filter indices by type (active or passive) and use pagination to navigate through results.
    """
    args_schema = IndicesToolInput

    def _run(
        self,
        indicesType: Optional[str] = None,
        limit: Optional[int] = 50,
        page: Optional[int] = 1
    ) -> str:
        """Run the tool to get indices data.
        
        Args:
            indicesType: Filter to return indices by type ('active' or 'passive')
            limit: Number of records to return per page
            page: Page number for pagination
            
        Returns:
            str: A formatted string containing the indices data
        """
        try:
            params = {
                'indicesType': indicesType,
                'limit': limit,
                'page': page
            }
            
            # Remove None values
            params = {k: v for k, v in params.items() if v is not None}
            
            response = self.client.base_endpoint._request("get", "/indices", params=params)
            
            # Format the response as a readable string
            if isinstance(response, dict) and 'data' in response:
                indices = response['data']
                if not indices:
                    return "No indices found for the specified criteria."
                
                result = []
                for index in indices:
                    analysis = [
                        f"ID: {index.get('ID', 0)}",
                        f"Name: {index.get('NAME', 'Unknown')}",
                        f"Ticker: {index.get('TICKER', 'Unknown')}",
                        f"Price: ${float(index.get('PRICE', 0)):.3f}",
                        f"Coins: {index.get('COINS', 0)}",
                        "\nPerformance:",
                        f"  24h: {float(index.get('24H', 0)):.2f}%",
                        f"  7d: {float(index.get('7D', 0)):.2f}%",
                        f"  1m: {float(index.get('1M', 0)):.2f}%",
                        f"  All-time: {float(index.get('ALL_TIME', 0)):.2f}%",
                        "\nMetrics:",
                        f"  24h Volume: ${float(index.get('24H_VOLUME', 0)):,.2f}",
                        f"  Market Cap: ${float(index.get('MARKET_CAP', 0)):,.2f}",
                        f"  Index Grade: {float(index.get('INDEX_GRADE', 0)):.2f}"
                    ]
                    
                    # Add top gainers if available
                    top_gainers = index.get('TOP_GAINERS_ICONS', {})
                    if top_gainers:
                        analysis.append("\nTop Gainers:")
                        for token_id, token_info in list(top_gainers.items())[:5]:  # Limit to 5 top gainers
                            analysis.append(f"  {token_info.get('name', 'Unknown')} (ID: {token_id})")
                    
                    result.append("\n".join(analysis))
                
                # Add pagination info
                pagination = response.get('pagination', {})
                total = pagination.get('total', 0)
                total_pages = pagination.get('totalPages', 0)
                
                summary = [
                    f"\nPagination:",
                    f"  Total Indices: {total}",
                    f"  Total Pages: {total_pages}",
                    f"  Current Page: {page}"
                ]
                
                return "\n\n" + "\n\n---\n\n".join(result) + "\n\n" + "\n".join(summary)
            
            return str(response)
            
        except Exception as e:
            return self._handle_error(e)
    
    def _arun(self, **kwargs) -> str:
        """Async implementation of the tool (not implemented)."""
        raise NotImplementedError("Async version not implemented") 