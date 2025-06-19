from typing import Optional
from pydantic import Field, field_validator, ValidationInfo
from datetime import datetime

from .base_tool import TMBaseTool, TMBaseToolInput

class SectorIndicesPerformanceToolInput(TMBaseToolInput):
    """Input schema for the Sector Indices Performance tool."""
    id: str = Field(
        ...,
        description="Id of the index. Example 1"
    )
    start_date: str = Field(
        ...,
        description="Start date in YYYY-MM-DD format"
    )
    end_date: str = Field(
        ...,
        description="End date in YYYY-MM-DD format"
    )
    limit: Optional[int] = Field(
        50,
        description="Number of records to return per page"
    )
    page: Optional[int] = Field(
        1,
        description="Page number for pagination"
    )


class SectorIndicesPerformanceTool(TMBaseTool):
    """Tool for analyzing sector indices performance metrics."""
    
    name: str = "analyze_sector_indices_performance"
    description: str = """Analyze the performance metrics of sector-specific cryptocurrency indices.
    Useful when you need to:
    - Track sector performance
    - Compare sector returns
    - Analyze risk metrics
    - Study volatility patterns
    - Monitor sector trends
    - Evaluate sector strength
    
    The tool provides detailed performance metrics including:
    - Total returns
    - Risk-adjusted returns
    - Volatility measures
    - Maximum drawdown
    - Sharpe ratio
    - Beta and alpha
    - Historical trends
    
    You can analyze:
    - Specific sector indices
    - Time periods
    - Return patterns
    - Risk metrics
    - Performance attribution
    - Comparative analysis
    
    Note: Requires id and date range (YYYY-MM-DD format).
    """
    args_schema = SectorIndicesPerformanceToolInput

    def _run(
        self,
        id: str,
        start_date: str,
        end_date: str,
        limit: Optional[int] = 50,
        page: Optional[int] = 1
    ) -> str:
        """Run the tool to analyze sector indices performance.
        
        Args:
            id: Id of the index (e.g., "1")
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            limit: Number of records to return per page
            page: Page number for pagination
            
        Returns:
            str: A formatted string containing the performance analysis
        """
        try:
            params = {
                'id': id,
                'start_date': start_date,
                'end_date': end_date,
                'limit': limit,
                'page': page
            }
            
            # Remove None values
            params = {k: v for k, v in params.items() if v is not None}
            
            response = self.client.base_endpoint._request("get", "/indices-performance", params=params)
            
            # Format the response as a readable string
            if isinstance(response, dict) and 'data' in response:
                performance = response['data']
                if not performance:
                    return "No performance data found for the specified criteria."
                
                result = []
                for period in performance:
                    analysis = [
                        f"ID: {period.get('ID', 0)}",
                        f"Date: {period.get('DATE', 'Unknown')}",
                        "\nPerformance Metrics:",
                        f"  Cumulative ROI: {float(period.get('INDEX_CUMULATIVE_ROI', 0)):.2f}%",
                        f"  Market Cap: ${float(period.get('MARKET_CAP', 0)):,.2f}",
                        f"  Volume: ${float(period.get('VOLUME', 0)):,.2f}",
                        f"  FDV: ${float(period.get('FDV', 0)):,.2f}"
                    ]
                    
                    # Add pagination info if available
                    pagination = period.get('pagination', {})
                    if pagination:
                        analysis.extend([
                            "\nPagination Info:",
                            f"  Total Records: {pagination.get('total', 0)}",
                            f"  Total Pages: {pagination.get('totalPages', 0)}"
                        ])
                    
                    result.append("\n".join(analysis))
                
              
                return "\n\n" + "\n\n---\n\n".join(result)
            
            return str(response)
            
        except Exception as e:
            return self._handle_error(e)
    
    def _arun(self, **kwargs) -> str:
        """Async implementation of the tool (not implemented)."""
        raise NotImplementedError("Async version not implemented") 