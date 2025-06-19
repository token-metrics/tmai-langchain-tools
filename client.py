import os
import sys 
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from base import BaseEndpoint
from tools.tokens import TokensTool
from tools.hourly_ohlcv import HourlyOHLCVTool
from tools.daily_ohlcv import DailyOHLCVTool
from tools.investor_grades import InvestorGradesTool
from tools.trader_grades import TraderGradesTool
from tools.market_metrics import MarketMetricsTool
from tools.trading_signals import TradingSignalsTool
from tools.resistance_support import ResistanceSupportTool
from tools.price import PriceTool
from tools.sentiment import SentimentTool
from tools.quantmetrics import QuantmetricsTool
from tools.scenario_analysis import ScenarioAnalysisTool
from tools.correlation import CorrelationTool
from tools.crypto_investors import CryptoInvestorsTool
from tools.top_tokens import TopTokensTool
from tools.sector_indices_holdings import SectorIndicesHoldingsTool
from tools.sector_indices_performance import SectorIndicesPerformanceTool
from tools.indices import IndicesTool
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from typing import Dict, Any, List
import json
load_dotenv()

class TokenMetricsClient:
    """Main client for interacting with the Token Metrics AI API."""
    
    BASE_URL = "https://api.tokenmetrics.com/v2"
    
    def __init__(self, api_key=None, base_url=None):
        """Initialize the Token Metrics client.
        
        Args:
            api_key (str): Your Token Metrics API key
            base_url (str, optional): Custom base URL for the API
        """
        self.api_key = api_key or os.getenv('TMAI_API_KEY')
        # print(f">>>>>>>>>>>>>>>>>>{self.api_key}")
        self.base_url = base_url or self.BASE_URL
        self.base_endpoint = BaseEndpoint(self,)
                
        self.tokens = TokensTool(self)
        self.trader_grades = TraderGradesTool(self)
        self.hourly_ohlcv = HourlyOHLCVTool(self)
        self.daily_ohlcv = DailyOHLCVTool(self)
        self.investor_grades = InvestorGradesTool(self)
        self.market_metrics = MarketMetricsTool(self)        
        self.trading_signals = TradingSignalsTool(self)                        
        self.crypto_investors = CryptoInvestorsTool(self)
        self.top_tokens = TopTokensTool(self)
        self.resistance_support = ResistanceSupportTool(self)
        self.price = PriceTool(self)
        self.sentiment = SentimentTool(self)
        self.quantmetrics = QuantmetricsTool(self)
        self.scenario_analysis = ScenarioAnalysisTool(self)
        self.correlation = CorrelationTool(self)        
        self.sector_indices_holdings = SectorIndicesHoldingsTool(self)
        self.sector_indices_performance = SectorIndicesPerformanceTool(self)        
        self.indices = IndicesTool(self)

def format_intermediate_steps(steps: List[Dict[str, Any]]) -> str:
    """Format intermediate steps (tool interactions) into a readable string."""
    formatted = []
    for step in steps:
        # Format the action
        action = step.get('action', {})
        tool_name = action.get('tool', '')
        tool_input = action.get('tool_input', {})
        if isinstance(tool_input, str):
            try:
                tool_input = eval(tool_input)  # Convert string repr of dict to dict
            except:
                tool_input = {"input": tool_input}
                
        formatted.append(f"""```blue{{Tool: {tool_name}
Input Parameters:
    {json.dumps(tool_input, indent=4)}}}```""")
        
        # Format the observation (response)
        observation = step.get('observation', '')
        if observation:
            if isinstance(observation, str):
                try:
                    observation = json.loads(observation)
                except:
                    observation = {"output": observation}
            
            formatted.append(f"""```yellow{{Output:
    {json.dumps(observation, indent=4)}}}```""")
            
    return "\n".join(formatted)

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()    
    client = TokenMetricsClient(api_key=os.getenv('TMAI_API_KEY'))
    # Simple coverage validation for REST API wrappers.
    # Each call will print whether a response was received (not None or empty).
    # This is not a unit test, but a basic check for endpoint reachability and wrapper wiring.

    def check_response(name, response):
        # Check for explicit API URL in the response (indicating a failure)
        api_url = "https://api.tokenmetrics.com/v2"
        found_api_url = False

        # Check if response is a dict or list and contains the API URL
        def contains_api_url(obj):
            if isinstance(obj, dict):
                for v in obj.values():
                    if contains_api_url(v):
                        return True
            elif isinstance(obj, list):
                for item in obj:
                    if contains_api_url(item):
                        return True
            elif isinstance(obj, str):
                if api_url in obj:
                    return True
            return False

        if response:
            if contains_api_url(response):
                print(f"[FAIL] {name}: API URL found in response, indicating failure.")
                print("Response:", response)
            else:
                print(f"[PASS] {name}: Response received.")                
        else:
            print(f"[FAIL] {name}: No response or empty response.")

    tests = [
        ("tokens", lambda: client.tokens.run(symbol="BTC", limit=5, page=1)),
        ("trader_grades", lambda: client.trader_grades.run(symbol="BTC")),
        ("hourly_ohlcv", lambda: client.hourly_ohlcv.run(symbol="BTC", start_date="2023-06-01", end_date="2023-06-07")),
        ("daily_ohlcv", lambda: client.daily_ohlcv.run(symbol="BTC", start_date="2023-06-01", end_date="2023-06-07")),
        ("investor_grades", lambda: client.investor_grades.run(symbol="BTC")),
        ("market_metrics", lambda: client.market_metrics.run(start_date="2023-06-01", end_date="2023-06-07")),
        ("trading_signals", lambda: client.trading_signals.run(symbol="BTC")),
        ("ai_reports", lambda: client.ai_reports.run(token_id="3375")),
        ("crypto_investors", lambda: client.crypto_investors.run()),
        ("top_tokens", lambda: client.top_tokens.run(top_k=10)),
        ("resistance_support", lambda: client.resistance_support.run(symbol="BTC")),
        ("tmai_agent", lambda: client.tmai_agent.run(user_query="What is the current price of BTC?")),
        ("price", lambda: client.price.run(token_id="3375")),
        ("sentiment", lambda: client.sentiment.run(limit=10)),
        ("quantmetrics", lambda: client.quantmetrics.run(symbol="BTC", token_id="3375")),
        ("scenario_analysis", lambda: client.scenario_analysis.run(token_id="3375")),
        ("correlation", lambda: client.correlation.run(token_id="3375",)),
        ("sector_indices_holdings", lambda: client.sector_indices_holdings.run(id="1")),
        ("sector_indices_performance", lambda: client.sector_indices_performance.run(id="1", start_date="2023-06-01", end_date="2023-06-07")),
        ("indices", lambda: client.indices.run(indicesType="active")),
    ]

    for idx, (name, func) in enumerate(tests, 1):
        try:
            response = func()
            check_response(f"{idx}. {name}", response)
        except Exception as e:
            print(f"[ERROR] {idx}. {name}: Exception occurred - {e}")