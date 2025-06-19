from typing import Optional
from pydantic import Field
from datetime import datetime

from .base_tool import TMBaseTool, TMBaseToolInput

class InvestorGradesToolInput(TMBaseToolInput):
    """Input schema for the Investor Grades tool."""
    token_id: Optional[str] = Field(
        None,
        description="Comma-separated Token IDs (e.g., '3375' for BTC)"
    )
    start_date: Optional[str] = Field(
        None,
        description="Start date in YYYY-MM-DD format"
    )
    end_date: Optional[str] = Field(
        None,
        description="End date in YYYY-MM-DD format"
    )
    symbol: Optional[str] = Field(
        None,
        description="Comma-separated Token Symbols (e.g., 'BTC,ETH')"
    )
    category: Optional[str] = Field(
        None,
        description="Comma-separated category names"
    )
    exchange: Optional[str] = Field(
        None,
        description="Comma-separated exchange names"
    )
    marketcap: Optional[str] = Field(
        None,
        description="Minimum MarketCap in $"
    )
    fdv: Optional[str] = Field(
        None,
        description="Minimum fully diluted valuation in $"
    )
    volume: Optional[str] = Field(
        None,
        description="Minimum 24h trading volume in $"
    )
    investor_grade: Optional[str] = Field(
        None,
        description="Minimum TM Investor Grade"
    )

class InvestorGradesTool(TMBaseTool):
    """Tool for accessing long-term investment grades from Token Metrics."""
    
    name: str = "get_investor_grades"
    description: str = """Get comprehensive long-term investment grades for cryptocurrencies using Token Metrics' proprietary research methodology.
    Useful when you need to:
    - Evaluate cryptocurrencies for long-term investment potential
    - Analyze a token's fundamentals, technology, and valuation
    - Compare different cryptocurrencies based on various metrics
    - Get detailed scores for community, technology, security, and more
    
    The tool provides various grades and scores including:
    - TM Investor Grade: Overall long-term outlook
    - Fundamental Grade: Community, team, investors, tokenomics
    - Technology Grade: Code review, technology, security
    - Valuation Grade: Relative sector valuation
    - DeFi Usage Score: Project use in DeFi
    - Community Score: Community engagement
    - Security Score: Technology security
    And many more...
    
    You can filter by:
    - token_id: Comma-separated Token IDs
    - symbol: Token symbols
    - category: Token categories
    - exchange: Exchange names
    - marketcap: Minimum market cap
    - fdv: Minimum fully diluted value
    - volume: Minimum 24h volume
    - investor_grade: Minimum grade
    - start_date/end_date: Date range
    
    Note: Data is limited to 29-day periods at a time.
    """
    args_schema = InvestorGradesToolInput

    def _run(
        self,
        token_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        symbol: Optional[str] = None,
        category: Optional[str] = None,
        exchange: Optional[str] = None,
        marketcap: Optional[str] = None,
        fdv: Optional[str] = None,
        volume: Optional[str] = None,
        investor_grade: Optional[str] = None
    ) -> str:
        """Run the tool to get investor grades data.
        
        Args:
            token_id: Comma-separated Token IDs (e.g., "3375" for BTC)
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            symbol: Comma-separated Token Symbols (e.g., "BTC,ETH")
            category: Comma-separated category names
            exchange: Comma-separated exchange names
            marketcap: Minimum MarketCap in $
            fdv: Minimum fully diluted valuation in $
            volume: Minimum 24h trading volume in $
            investor_grade: Minimum TM Investor Grade
            
        Returns:
            str: A formatted string containing the investor grades data
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
            
            params = {
                'token_id': token_id,
                'start_date': start_date,
                'end_date': end_date,
                'symbol': symbol,
                'category': category,
                'exchange': exchange,
                'marketcap': marketcap,
                'fdv': fdv,
                'volume': volume,
                'investor_grade': investor_grade
            }
            
            # Remove None values
            params = {k: v for k, v in params.items() if v is not None}
            
            response = self.client.base_endpoint._request("get", "/investor-grades", params=params)
            
            # Format the response as a readable string
            if isinstance(response, dict) and 'data' in response:
                data = response['data']
                if not data:
                    return "No trader grades data found for the specified criteria."
                result = []
                for entry in data:
                    grades_info = [
                        f"Token ID: {entry.get('TOKEN_ID', 0)}",
                        f"Token: {entry.get('TOKEN_NAME', 'Unknown')} ({entry.get('TOKEN_SYMBOL', 'Unknown')})",
                        f"Date: {entry.get('DATE', 'Unknown')}",
                        f"TM Investor Grade: {entry.get('TM_INVESTOR_GRADE', 0)}",
                        f"7D Change: {entry.get('TM_INVESTOR_GRADE_7D_PCT_CHANGE', 0)}%",
                        "\nGrades:",
                        f"- Fundamental: {entry.get('FUNDAMENTAL_GRADE', 0)}",
                        f"- Technology: {entry.get('TECHNOLOGY_GRADE', 0)}",
                        f"- Valuation: {entry.get('VALUATION_GRADE', 0)}",
                        "\nDetailed Scores:",
                        f"- DeFi Usage: {entry.get('DEFI_USAGE_SCORE', 'Unknown')}",
                        f"- Tokenomics: {entry.get('TOKENOMICS_SCORE', 0)}",
                        f"- Community: {entry.get('COMMUNITY_SCORE', 0)}",
                        f"- Exchange: {entry.get('EXCHANGE_SCORE', 0)}",
                        f"- VC: {entry.get('VC_SCORE', 'Unknown')}",
                        f"- DeFi Scanner: {entry.get('DEFI_SCANNER_SCORE', 0)}",
                        f"- Activity: {entry.get('ACTIVITY_SCORE', 0)}",
                        f"- Repository: {entry.get('REPOSITORY_SCORE', 0)}",
                        f"- Collaboration: {entry.get('COLLABORATION_SCORE', 0)}",
                        f"- Security: {entry.get('SECURITY_SCORE', 0)}"
                    ]
                    result.append("\n".join(grades_info))
                
                return "\n\n".join(result)
            
            return str(response)
            
        except Exception as e:
            return self._handle_error(e)
    
    def _arun(self, **kwargs) -> str:
        """Async implementation of the tool (not implemented)."""
        raise NotImplementedError("Async version not implemented")
