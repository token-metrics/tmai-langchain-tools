from typing import Optional, Dict, Any
from pydantic import Field
from datetime import datetime

from .base_tool import TMBaseTool, TMBaseToolInput

class ScenarioAnalysisToolInput(TMBaseToolInput):
    """Input schema for the Scenario Analysis tool."""
    token_id: Optional[str] = Field(
        None,
        description="Comma separated token IDs to analyze"
    )
    symbol: Optional[str] = Field(
        None,
        description="Comma separated token symbols to analyze"
    )   
    limit: Optional[int] = Field(
        50,
        description="Number of records to return per page"
    )
    page: Optional[int] = Field(
        1,
        description="Page number for pagination"
    )

class ScenarioAnalysisTool(TMBaseTool):
    """Tool for accessing advanced scenario analysis and market simulation tools."""
    
    name: str = "analyze_market_scenarios"
    description: str = """Analyze different market scenarios and their potential impact on cryptocurrencies.
    Useful when you need to:
    - Simulate market crash scenarios
    - Analyze potential bull run impacts
    - Assess regulatory change effects
    - Evaluate technological breakthrough implications
    - Study macro event impacts
    - Create custom scenario analyses
    
    The tool provides comprehensive analysis including:
    - Price impact projections
    - Volume change forecasts
    - Volatility projections
    - Liquidity impact analysis
    - Risk metrics (VaR, Expected Shortfall)
    - Correlation analysis
    - Time series projections
    
    You can filter the analysis by:
    - Specific tokens (using token_id or symbol)
    - Number of results (using limit)
    - Page navigation (using page)
    """
    args_schema = ScenarioAnalysisToolInput

    def _run(
        self,
        token_id: Optional[str] = None,
        symbol: Optional[str] = None,      
        limit: Optional[int] = 50,
        page: Optional[int] = 1
    ) -> str:
        """Run the tool to get scenario analysis results.
        
        Args:
            token_id: Comma separated token IDs to analyze
            symbol: Comma separated token symbols to analyze
            limit: Number of records to return
            page: Page number for pagination
            
        Returns:
            str: A formatted string containing the scenario analysis results
        """
        try:         
            
            params = {
                'token_id': token_id,
                'symbol': symbol,
                'limit': limit,
                'page': page
            }
            
            # Remove None values
            params = {k: v for k, v in params.items() if v is not None}
            
            response = self.client.base_endpoint._request("get", "/scenario-analysis", params=params)
            
            # Format the response as a readable string
            if isinstance(response, dict) and 'data' in response:
                data = response['data']
                if not data:
                    return "No scenario analysis results found for the specified criteria."
                
                result = []
                for metric in data:
                    scenario_prediction = metric.get('SCENARIO_PREDICTION', {})
                    scenarios = scenario_prediction.get('scenario_prediction', [])
                    
                    # Handle potential string values safely
                    token_mcap = scenario_prediction.get('token_mcap', 0)
                    token_mcap = float(token_mcap) if token_mcap is not None else 0
                    
                    total_mcap = scenario_prediction.get('total_mcap', 0)
                    total_mcap = float(total_mcap) if total_mcap is not None else 0
                    
                    current_price = scenario_prediction.get('current_price', 0)
                    current_price = float(current_price) if current_price is not None else 0
                    
                    analysis = [
                        f"Token: {metric.get('TOKEN_NAME', 'Unknown')} ({metric.get('TOKEN_SYMBOL', 'Unknown')})",
                        f"ID: {metric.get('TOKEN_ID', 0)}",
                        f"Date: {metric.get('DATE', 'Unknown')}",
                        "\nCurrent Market Data:",
                        f"- Token Market Cap: ${token_mcap:,.2f}",
                        f"- Total Market Cap: ${total_mcap:,.2f}",
                        f"- Category: {scenario_prediction.get('category_name', 'Unknown')}",
                        f"- Current Price: ${current_price:,.2f}",
                        f"- Predicted Date: {scenario_prediction.get('predicted_date', 'Unknown')}"
                    ]
                    
                    if scenarios:
                        analysis.append("\nScenario Analysis:")
                        
                        for scenario in scenarios:
                            scenario_value = scenario.get('scenario', 0)
                            scenario_value = float(scenario_value) if scenario_value is not None else 0
                            
                            # Safely convert all numeric values
                            predicted_price_base = scenario.get('predicted_price_base', 0)
                            predicted_price_base = float(predicted_price_base) if predicted_price_base is not None else 0
                            
                            predicted_price_bear = scenario.get('predicted_price_bear', 0)
                            predicted_price_bear = float(predicted_price_bear) if predicted_price_bear is not None else 0
                            
                            predicted_price_moon = scenario.get('predicted_price_moon', 0)
                            predicted_price_moon = float(predicted_price_moon) if predicted_price_moon is not None else 0
                            
                            predicted_mcap_base = scenario.get('predicted_mcap_base', 0)
                            predicted_mcap_base = float(predicted_mcap_base) if predicted_mcap_base is not None else 0
                            
                            predicted_mcap_bear = scenario.get('predicted_mcap_bear', 0)
                            predicted_mcap_bear = float(predicted_mcap_bear) if predicted_mcap_bear is not None else 0
                            
                            predicted_mcap_moon = scenario.get('predicted_mcap_moon', 0)
                            predicted_mcap_moon = float(predicted_mcap_moon) if predicted_mcap_moon is not None else 0
                            
                            predicted_fdv_base = scenario.get('predicted_fdv_base', 0)
                            predicted_fdv_base = float(predicted_fdv_base) if predicted_fdv_base is not None else 0
                            
                            predicted_fdv_bear = scenario.get('predicted_fdv_bear', 0)
                            predicted_fdv_bear = float(predicted_fdv_bear) if predicted_fdv_bear is not None else 0
                            
                            predicted_fdv_moon = scenario.get('predicted_fdv_moon', 0)
                            predicted_fdv_moon = float(predicted_fdv_moon) if predicted_fdv_moon is not None else 0
                            
                            predicted_roi_base = scenario.get('predicted_roi_base', 0)
                            predicted_roi_base = float(predicted_roi_base) if predicted_roi_base is not None else 0
                            
                            predicted_roi_bear = scenario.get('predicted_roi_bear', 0)
                            predicted_roi_bear = float(predicted_roi_bear) if predicted_roi_bear is not None else 0
                            
                            predicted_roi_moon = scenario.get('predicted_roi_moon', 0)
                            predicted_roi_moon = float(predicted_roi_moon) if predicted_roi_moon is not None else 0
                            
                            total_mcap_scenario = scenario.get('total_mcap_scenario', 0)
                            total_mcap_scenario = float(total_mcap_scenario) if total_mcap_scenario is not None else 0
                            
                            analysis.extend([
                                f"\nScenario {scenario_value}x Market Cap:",
                                "\nPrice Predictions:",
                                f"- Base Case: ${predicted_price_base:,.2f}",
                                f"- Bear Case: ${predicted_price_bear:,.2f}",
                                f"- Moon Case: ${predicted_price_moon:,.2f}",
                                "\nMarket Cap Predictions:",
                                f"- Base Case: ${predicted_mcap_base:,.2f}",
                                f"- Bear Case: ${predicted_mcap_bear:,.2f}",
                                f"- Moon Case: ${predicted_mcap_moon:,.2f}",
                                "\nFDV Predictions:",
                                f"- Base Case: ${predicted_fdv_base:,.2f}",
                                f"- Bear Case: ${predicted_fdv_bear:,.2f}",
                                f"- Moon Case: ${predicted_fdv_moon:,.2f}",
                                "\nROI Predictions:",
                                f"- Base Case: {predicted_roi_base*100:,.2f}%",
                                f"- Bear Case: {predicted_roi_bear*100:,.2f}%",
                                f"- Moon Case: {predicted_roi_moon*100:,.2f}%",
                                f"\nTotal Market Cap in Scenario: ${total_mcap_scenario:,.2f}"
                            ])
                    
                    # Add past performance metrics with safe conversion
                    avg_past_performance = scenario_prediction.get('avg_past_performance', 0)
                    avg_past_performance = float(avg_past_performance) if avg_past_performance is not None else 0
                    
                    self_past_performance = scenario_prediction.get('self_past_performance', 0)
                    self_past_performance = float(self_past_performance) if self_past_performance is not None else 0
                    
                    analysis.extend([
                        "\nHistorical Performance:",
                        f"- Average Past Performance: {avg_past_performance*100:,.2f}%",
                        f"- Self Past Performance: {self_past_performance*100:,.2f}%"
                    ])
                    
                    # Add similar tokens info if available
                    similar_tokens = scenario_prediction.get('similar_tokens_info')
                    if similar_tokens and similar_tokens != "null":
                        analysis.append(f"\nSimilar Tokens: {similar_tokens}")
                    
                    result.append("\n".join(analysis))
                
                return "\n\n" + "\n\n---\n\n".join(result)
            
            return str(response)
            
        except Exception as e:
            return self._handle_error(e)
    
    def _arun(self, **kwargs) -> str:
        """Async implementation of the tool (not implemented)."""
        raise NotImplementedError("Async version not implemented") 