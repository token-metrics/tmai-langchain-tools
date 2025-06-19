# Token Metrics AI LangChain Tools

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-Compatible-green.svg)](https://langchain.com/)

A comprehensive suite of LangChain-compatible tools for integrating Token Metrics AI API capabilities into your AI agents and applications. This library provides 21+ specialized tools for cryptocurrency analysis, market intelligence, and trading insights that seamlessly integrate with LangChain's agent framework.

## 🚀 Features

- **18 LangChain Tools** for comprehensive crypto analysis
- **Type-Safe** - Full Pydantic model validation for all inputs
- **Error Handling** - Robust error handling with user-friendly messages
- **Pagination Support** - Automatic handling of large datasets
- **Rate Limiting** - Built-in respect for API rate limits
- **Comprehensive Documentation** - Detailed tool descriptions and examples

## 📦 Installation

```bash
pip install -r requirements.txt
```

### Dependencies

```bash
pip install langchain pydantic requests python-dotenv
```

## 🔧 Quick Start

### 1. Setup API Key

```python
import os
from dotenv import load_dotenv

# Option 1: Environment variable
os.environ["TMAI_API_KEY"] = "your_api_key_here"

# Option 2: .env file
load_dotenv()  # Requires TMAI_API_KEY=your_api_key_here in .env
```

### 2. Initialize Client and Tools

```python
from client import TokenMetricsClient

# Initialize client
client = TokenMetricsClient()

# Access individual tools
price_tool = client.price
tokens_tool = client.tokens
trading_signals_tool = client.trading_signals
```

### 3. Basic Usage

```python
# Get current BTC price
btc_price = client.price.run(token_id="3375")
print(btc_price)

# Get top 10 tokens by market cap
top_tokens = client.top_tokens.run(top_k=10)
print(top_tokens)

# Get trading signals for ETH
eth_signals = client.trading_signals.run(symbol="ETH")
print(eth_signals)
```

## 🤖 LangChain Agent Integration

### Simple Agent Example

```python
from langchain.agents import AgentType, initialize_agent
from langchain.llms import OpenAI
from client import TokenMetricsClient

# Initialize Token Metrics client
tm_client = TokenMetricsClient()

# Create tools list for agent
tools = [
    tm_client.price,
    tm_client.trading_signals,
    tm_client.trader_grades,
    tm_client.market_metrics,
    tm_client.sentiment,
    tm_client.correlation,
]

# Initialize LLM
llm = OpenAI(temperature=0)

# Create agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Use the agent
response = agent.run(
    "What is the current price of Bitcoin and should I buy it based on trading signals?"
)
print(response)
```

### Advanced Agent Example

```python
from langchain.agents import AgentType, initialize_agent
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from client import TokenMetricsClient

# Initialize with full tool suite
tm_client = TokenMetricsClient()

# Comprehensive tool set for crypto analysis
crypto_analysis_tools = [
    # Price and market data
    tm_client.price,
    tm_client.tokens,
    tm_client.top_tokens,
    tm_client.market_metrics,
    
    # Trading analysis
    tm_client.trading_signals,
    tm_client.trader_grades,
    tm_client.investor_grades,
    tm_client.resistance_support,
    
    # Technical analysis
    tm_client.daily_ohlcv,
    tm_client.hourly_ohlcv,
    tm_client.correlation,
    tm_client.quantmetrics,
    
    # Market intelligence
    tm_client.sentiment,
    tm_client.ai_reports,
    tm_client.scenario_analysis,
    tm_client.crypto_investors,
    
    # Index analysis
    tm_client.indices,
    tm_client.sector_indices_holdings,
    tm_client.sector_indices_performance,
    tm_client.trader_indices,
    
    # AI agent
    tm_client.ai_agent,
]

# Initialize agent with memory
memory = ConversationBufferMemory(memory_key="chat_history")

agent = initialize_agent(
    tools=crypto_analysis_tools,
    llm=OpenAI(temperature=0),
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# Complex analysis query
response = agent.run("""
Perform a comprehensive analysis of Ethereum:
1. Get current price and recent OHLCV data
2. Check trading signals and grades
3. Analyze market sentiment
4. Look at correlation with Bitcoin
5. Provide investment recommendation
""")
```

## 🛠️ Available Tools

### Market Data Tools

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `price` | Get current cryptocurrency prices | `token_id` |
| `tokens` | Search and get token information | `symbol`, `token_name`, `category` |
| `top_tokens` | Get top tokens by market cap | `top_k` |
| `daily_ohlcv` | Daily OHLCV price data | `token_id`, `symbol`, `start_date`, `end_date` |
| `hourly_ohlcv` | Hourly OHLCV price data | `token_id`, `symbol`, `start_date`, `end_date` |

### Trading & Analysis Tools

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `trading_signals` | AI-generated trading signals | `token_id`, `symbol`, `signal`, `start_date`, `end_date` |
| `trader_grades` | Short-term trading grades | `token_id`, `symbol`, `trader_grade` |
| `investor_grades` | Long-term investment grades | `token_id`, `symbol`, `investor_grade` |
| `resistance_support` | Support and resistance levels | `token_id`, `symbol` |
| `correlation` | Token correlation analysis | `token_id`, `symbol`, `category` |
| `quantmetrics` | Quantitative metrics and ratios | `token_id`, `symbol`, `marketcap`, `volume` |

### Market Intelligence Tools

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `market_metrics` | Overall market sentiment metrics | `start_date`, `end_date` |
| `sentiment` | Multi-platform sentiment analysis | `limit`, `page` |
| `ai_reports` | AI-generated market reports | `token_id`, `symbol` |
| `scenario_analysis` | Market scenario simulations | `token_id`, `symbol` |
| `crypto_investors` | Institutional investor data | `limit`, `page` |

### Index & Portfolio Tools

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `indices` | Cryptocurrency indices data | `indicesType`, `limit`, `page` |
| `sector_indices_holdings` | Index composition and holdings | `id` |
| `sector_indices_performance` | Index performance metrics | `id`, `start_date`, `end_date` |
| `trader_indices` | AI trading portfolio indices | `index_type`, `strategy`, `risk_profile` |

### AI Tools

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `ai_agent` | Natural language AI analysis | `user_query` |

## 📖 Tool Reference Guide

### Price Tool

```python
# Get current price for Bitcoin
price = client.price.run(token_id="3375")  # Bitcoin token ID

# Get prices for multiple tokens
prices = client.price.run(token_id="3375,1027")  # BTC,ETH
```

### Trading Signals Tool

```python
# Get current trading signals for ETH
signals = client.trading_signals.run(symbol="ETH")

# Get bullish signals only
bullish_signals = client.trading_signals.run(
    symbol="BTC,ETH",
    signal="1"  # 1=bullish, -1=bearish, 0=neutral
)

# Get signals for a date range
historical_signals = client.trading_signals.run(
    symbol="BTC",
    start_date="2024-01-01",
    end_date="2024-01-31"
)
```

### AI Agent Tool

```python
# Natural language analysis
analysis = client.ai_agent.run(
    user_query="What are the best DeFi tokens to invest in right now?"
)

# Complex multi-part query
detailed_analysis = client.ai_agent.run(
    user_query="""
    Analyze the current market conditions and recommend a portfolio 
    allocation strategy for a moderate risk investor with $10,000 
    looking for 6-month investments.
    """
)
```

### Market Metrics Tool

```python
# Get current market metrics
metrics = client.market_metrics.run()

# Get historical market metrics
historical_metrics = client.market_metrics.run(
    start_date="2024-01-01",
    end_date="2024-01-31"
)
```

## 🎯 Common Agent Use Cases

### 1. Portfolio Analysis Agent

```python
portfolio_tools = [
    tm_client.tokens,
    tm_client.trader_grades,
    tm_client.investor_grades,
    tm_client.correlation,
    tm_client.scenario_analysis,
]

agent = initialize_agent(portfolio_tools, llm, AgentType.ZERO_SHOT_REACT_DESCRIPTION)

# Analyze portfolio diversification
response = agent.run(
    "Analyze the correlation between BTC, ETH, and SOL. "
    "Recommend optimal portfolio weights for risk diversification."
)
```

### 2. Trading Signal Agent

```python
trading_tools = [
    tm_client.trading_signals,
    tm_client.trader_grades,
    tm_client.resistance_support,
    tm_client.daily_ohlcv,
    tm_client.sentiment,
]

agent = initialize_agent(trading_tools, llm, AgentType.ZERO_SHOT_REACT_DESCRIPTION)

# Get trading recommendations
response = agent.run(
    "Should I buy or sell ETH today? Consider technical signals, "
    "support/resistance levels, and market sentiment."
)
```

### 3. Market Research Agent

```python
research_tools = [
    tm_client.ai_reports,
    tm_client.crypto_investors,
    tm_client.market_metrics,
    tm_client.sentiment,
    tm_client.top_tokens,
]

agent = initialize_agent(research_tools, llm, AgentType.ZERO_SHOT_REACT_DESCRIPTION)

# Market research query
response = agent.run(
    "What are the current market trends? Which tokens are institutional "
    "investors buying? What's the overall market sentiment?"
)
```

## 🔍 Error Handling

All tools include comprehensive error handling:

```python
try:
    # This will handle API errors gracefully
    data = client.tokens.run(symbol="INVALID_SYMBOL")
except Exception as e:
    print(f"Error: {e}")
    # Agent can continue with fallback logic
```

## ⚙️ Configuration

### Environment Variables

```bash
# Required
TMAI_API_KEY=your_token_metrics_api_key

# Optional
TMAI_BASE_URL=https://api.tokenmetrics.com  # Default API base URL
```

### Client Configuration

```python
# Custom configuration
client = TokenMetricsClient(
    api_key="your_key",
    base_url="https://api.tokenmetrics.com"  # Custom base URL
)
```

## 📚 Best Practices

### 1. Tool Selection for Agents

Choose tools based on your agent's purpose:

- **Trading Bots**: `trading_signals`, `trader_grades`, `resistance_support`
- **Investment Advisors**: `investor_grades`, `ai_reports`, `scenario_analysis`
- **Market Analysts**: `market_metrics`, `sentiment`, `correlation`
- **Portfolio Managers**: `correlation`, `quantmetrics`, `indices`

### 2. Rate Limiting

```python
import time

# Add delays between API calls in loops
for symbol in ["BTC", "ETH", "SOL"]:
    data = client.trader_grades.run(symbol=symbol)
    time.sleep(1)  # Respect rate limits
```

### 3. Error Recovery

```python
def get_token_analysis(symbol):
    try:
        return client.ai_agent.run(f"Analyze {symbol}")
    except Exception as e:
        # Fallback to basic data
        return client.tokens.run(symbol=symbol)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- [LangChain](https://github.com/langchain-ai/langchain) - Framework for developing applications powered by language models
- [Token Metrics](https://tokenmetrics.com) - AI-driven cryptocurrency analytics platform

---

**Disclaimer**: This library provides tools for accessing Token Metrics AI API. Please refer to Token Metrics' terms of service and API documentation for usage guidelines and limitations. Always conduct your own research before making investment decisions. 