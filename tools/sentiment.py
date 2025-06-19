from typing import Optional
from pydantic import Field

from .base_tool import TMBaseTool, TMBaseToolInput

class SentimentToolInput(TMBaseToolInput):
    """Input schema for the Sentiment Analysis tool."""
    limit: Optional[int] = Field(
        50,
        description="Limit the number of items in response"
    )
    page: Optional[int] = Field(
        1,
        description="Page number for pagination"
    )

class SentimentTool(TMBaseTool):
    """Tool for accessing market sentiment analysis from Token Metrics."""
    
    name: str = "get_market_sentiment"
    description: str = """Get comprehensive market sentiment analysis from Twitter, Reddit, and News sources.
    Useful when you need to:
    - Understand overall crypto market sentiment
    - Track sentiment across different platforms
    - Get summaries of market discussions
    - Monitor sentiment changes
    
    The tool provides sentiment analysis from multiple sources:
    - Overall Market Sentiment
    - News Sentiment (with summaries)
    - Reddit Sentiment (with discussion summaries)
    - Twitter Sentiment (with discussion summaries)
    
    Sentiment is scored from -1 (Very Negative) to 1 (Very Positive).
    Data is updated hourly.
    
    You can control the amount of data with:
    - limit: Number of items to return (default: 50)
    - page: Page number for pagination (default: 1)
    """
    args_schema = SentimentToolInput

    def _run(
        self,
        limit: Optional[int] = 50,
        page: Optional[int] = 1
    ) -> str:
        """Run the tool to get sentiment analysis data.
        
        Args:
            limit: Limit the number of items in response
            page: Page number for pagination
            
        Returns:
            str: A formatted string containing the sentiment analysis data
        """
        try:
            params = {
                'limit': limit,
                'page': page
            }
            
            # Remove None values
            params = {k: v for k, v in params.items() if v is not None}
            
            response = self.client.base_endpoint._request("get", "/sentiments", params=params)
            
            # Format the response as a readable string
            if isinstance(response, dict) and 'data' in response:
                data = response['data']
                if not data:
                    return "No sentiment data found."
                
                result = []
                for entry in data:
                    sentiment_info = [
                        f"Time: {entry.get('DATETIME', 'Unknown')}",
                        "\nOverall Market Sentiment:",
                        f"- Grade: {entry.get('MARKET_SENTIMENT_GRADE', 0)}",
                        f"- Label: {entry.get('MARKET_SENTIMENT_LABEL', 'Unknown')}",
                        "\nNews Sentiment:",
                        f"- Grade: {entry.get('NEWS_SENTIMENT_GRADE', 0)}",
                        f"- Label: {entry.get('NEWS_SENTIMENT_LABEL', 'Unknown')}",
                        f"- Summary: {entry.get('NEWS_SUMMARY', 'No summary available')}",
                        "\nReddit Sentiment:",
                        f"- Grade: {entry.get('REDDIT_SENTIMENT_GRADE', 0)}",
                        f"- Label: {entry.get('REDDIT_SENTIMENT_LABEL', 'Unknown')}",
                        f"- Summary: {entry.get('REDDIT_SUMMARY', 'No summary available')}",
                        "\nTwitter Sentiment:",
                        f"- Grade: {entry.get('TWITTER_SENTIMENT_GRADE', 0)}",
                        f"- Label: {entry.get('TWITTER_SENTIMENT_LABEL', 'Unknown')}",
                        f"- Summary: {entry.get('TWITTER_SUMMARY', 'No summary available')}"
                    ]
                    result.append("\n".join(sentiment_info))
                
                return "\n\n" + "\n\n---\n\n".join(result)
            
            return str(data)
            
        except Exception as e:
            return self._handle_error(e)
    
    def _arun(self, **kwargs) -> str:
        """Async implementation of the tool (not implemented)."""
        raise NotImplementedError("Async version not implemented") 