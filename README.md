# Financial Assistant Chatbot

An intelligent stock analysis chatbot powered by OpenAI's GPT-4 and real-time financial data from Yahoo Finance. Built with Streamlit for an interactive user experience.

##  Features

- **Real-time Stock Prices**: Get current stock prices 
- **Technical Analysis Tools**:
  - Simple Moving Average (SMA)
  - Exponential Moving Average (EMA)
  - Relative Strength Index (RSI)
  - Moving Average Convergence Divergence (MACD)
- **Interactive Price Charts**: Visualize stock price trends over time
- **Natural Language Interface**: Ask questions in plain English and get intelligent responses

##  Technology Used

- **Python 3.x**
- **OpenAI GPT-4o-mini**: Powers the conversational AI
- **Streamlit**: Web application framework
- **yfinance**: Fetches real-time stock market data
- **pandas**: Data manipulation and analysis
- **matplotlib**: Data visualization

## Prerequisites

- Python 3.7 or higher
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/financial-chatbot.git
cd financial-chatbot
```

2. Install required dependencies:
```bash
pip install openai pandas matplotlib streamlit yfinance
```

3. Create an `API_KEY` file in the project root directory and add your OpenAI API key:
```
your-openai-api-key-here
```

##  Usage

1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the provided local URL (typically `http://localhost:8501`)

3. Start asking questions about stocks! Example queries:
   - "What's the current price of AAPL?"
   - "Calculate the RSI for TSLA"
   - "Show me the 50-day moving average for MSFT"
   - "Plot the stock price for GOOGL"

##  Key Functions

| Function | Description |
|----------|-------------|
| `get_stock_price(ticker)` | Retrieves the latest closing price |
| `calcuate_SMA(ticker, window)` | Calculates Simple Moving Average |
| `calcuate_EMA(ticker, window)` | Calculates Exponential Moving Average |
| `calculateRSI(ticker)` | Computes Relative Strength Index |
| `calculate_MACD(ticker)` | Calculates MACD indicator |
| `plot_stock_price(ticker)` | Generates price chart visualization |

##  Example Questions

- "What is Tesla's stock price?"
- "Calculate the 20-day SMA for Apple"
- "What's the RSI for Microsoft?"
- "Show me Amazon's MACD"
- "Plot the stock price for Netflix"

##  Contributors

- [Sara Avila]
- [Ashlyn Viereck]

##  Course Info

Final Project for Generative AI Course  
[Creighton University] - [Fall / 2025]

