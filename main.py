import json
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf
from openai import OpenAI

client = OpenAI(api_key=open('API_KEY', 'r').read().strip())

def get_stock_price(ticker):
    return str(yf.Ticker(ticker).history(period='1y').iloc[-1].Close)

def calcuate_SMA(ticker, window):
    data = yf.Ticker(ticker).history(period='1y').Close
    return str(data.rolling(window=window).mean().iloc[-1])

def calcuate_EMA(ticker, window):
    data = yf.Ticker(ticker).history(period='1y').Close
    return str(data.ewm(span=window, adjust=False).mean().iloc[-1]) 

def calcuate_RSI(ticker):
    data = yf.Ticker(ticker).history(period='1y').Close
    delta = data.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(com=13, adjust=False).mean()
    eama_down = down.ewm(com=13, adjust=False).mean()
    rs = ema_up / eama_down
    return str(100 - (100 / (1 + rs)).iloc[-1])

def calculate_MACD(ticker):
    data = yf.Ticker(ticker).history(period='1y').Close
    short_EMA = data.ewm(span=12, adjust=False).mean()
    long_EMA = data.ewm(span=26, adjust=False).mean()

    MACD = short_EMA - long_EMA
    signal = MACD.ewm(span=9, adjust=False).mean()

    MACD_histofram = MACD - signal

    return f'{MACD[-1], {signal[-1]}, {MACD_histofram[-1]}}'

def plot_stock_price(ticker):
    data = yf.Ticker(ticker).history(period='1y')
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data.values)
    plt.title(f'{ticker} Stock Price Over the Last Year')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    plt.savefig('stock_price.png')
    plt.close()

functions = [
    {
        'name': 'get_stock_price',
        'description': 'Gets the latest stock price given the ticker symbol of a company.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (for example AAPL for Apple).'
                }
            },
            'required': ['ticker']
        }
    },
    {
        'name': 'calcuate_SMA',
        'description': 'Calculates the Simple Moving Average (SMA) for a given stock ticker and a window.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (e.g., AAPL for Apple).'
                },
                'window': {
                    'type': 'integer',
                    'description': 'The timeframe to consider when calcualating the SMA.'
                }
            },
            'required': ['ticker', 'window']
        }
    },
    {
        'name': 'calcuate_EMA',
        'description': 'Calculates the Exponential Moving Average (EMA) for a given stock ticker and a window.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (e.g., AAPL for Apple).'
                },
                'window': {
                    'type': 'integer',
                    'description': 'The timeframe to consider when calcualating the EMA.'
                }
            },
            'required': ['ticker', 'window']
        }
    },
    {
        'name': 'calcuate_RSI',
        'description': 'Calculates the Relative Strength Index (RSI) for a given stock ticker.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (e.g., AAPL for Apple).'
                }
            },
            'required': ['ticker']
        }
    },
    {
        'name': 'calculate_MACD',
        'description': 'Calculates the Moving Average Convergence Divergence (MACD) for a given stock ticker.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (e.g., AAPL for Apple).'
                }
            },
            'required': ['ticker']
        }
    },
    {
        'name': 'plot_stock_price',
        'description': 'Plots the stock price for the last year given the stock ticker symbol of a company.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (e.g., AAPL for Apple).'
                }
            },
            'required': ['ticker']
        }

    }
]

available_functions = {
    'get_stock_price': get_stock_price,
    'calcuate_SMA': calcuate_SMA,
    'calcuate_EMA': calcuate_EMA,
    'calcuate_RSI': calcuate_RSI,
    'calculate_MACD': calculate_MACD,
    'plot_stock_price': plot_stock_price
}

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

st.title('Stock Analysis Chatbot Assistant')

user_input = st.text_input('Your question:')

if user_input:
    try: 
        st.session_state['messages'].append({'role': 'user', 'content': user_input})

        completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state["messages"],
        functions=functions,
        function_call="auto"
    )

        msg = completion.choices[0].message

        if msg.function_call:
            fn_name = msg.function_call.name
            args = json.loads(msg.function_call.arguments)

            fn = available_functions[fn_name]
            result = fn(**args)

            st.session_state["messages"].append(msg)
            st.session_state["messages"].append({
                "role": "function",
                "name": fn_name,
                "content": result
            })
            
            if fn_name == "plot_stock_price":
                st.image("stock_price.png")
            else:
                completion2 = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state["messages"]
                )
                final_msg = completion2.choices[0].message["content"]
                st.write(final_msg)
                st.session_state["messages"].append({"role": "assistant", "content": final_msg})
        else:
            st.write(msg["content"])
            st.session_state["messages"].append({"role": "assistant", "content": msg["content"]})
    except Exception as e:
        raise e
