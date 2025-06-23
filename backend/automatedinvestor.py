# Import libraries we need
import pandas as pd  # For data handling (not used in this code)
import requests as rq  # For making web requests
from bs4 import BeautifulSoup as bs  # For parsing HTML
import schedule  # For scheduling tasks (not used in this code)
import time  # For adding delays
import re  # For text pattern matching
from dotenv import load_dotenv
import google.generativeai as genai
import yfinance as yf
import alpaca_trade_api as tradeapi
from datetime import datetime
import yfinance as yf
import json
import os

load_dotenv()  

# Initialize API
api = tradeapi.REST(
    os.getenv('APCA_API_KEY_ID'), 
    os.getenv('APCA_API_SECRET_KEY'), 
    'https://paper-api.alpaca.markets', 
    api_version='v2'
)

# Create data directory path relative to current file
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def invest(unparsed_tickers):
    account = api.get_account()
    parsed_tickers = parse_tickers_from_string(unparsed_tickers)
    
    # Temporary function call just to calculate the past prices of 1 ticker
    try:
        for i in range(len(parsed_tickers)):
            calculate_dip(parsed_tickers[i])
            print('This is the price of '+parsed_tickers[i])
    except IndexError:
        print("No tickers in the list")
    except Exception as e:
        print(f"Error processing tickers: {e}")
    
    sell_stock()
    portfolio_info()
    return

def parse_tickers_from_string(text):
    pattern = r'\$?([A-Z]{1,5})\b'
    tickers = re.findall(pattern, text)
    return list(set(tickers))

def calculate_dip(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        current_price = info.get('currentPrice')
        yesterday_price = get_price_yesterday(ticker)
        
        if yesterday_price is not None and current_price is not None:
            if (current_price <= (yesterday_price * 0.95)):
                buy_stock(ticker)
            else:
                print(f'{ticker} not bought')
        else:
            print(f'{ticker} skipped - could not get yesterday\'s price')

        print('This is the price now: ' + str(current_price) + ' and this is the price three days ago: '+ str(yesterday_price))
    
    except Exception as e:
        print(f"Error calculating dip for {ticker}: {e}")

    return

def get_price_yesterday(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period='5d')

        if not hist.empty:
            last_close = hist['Close'].iloc[-3]
            return round(last_close, 2)
    except Exception as e:
        print(f"Error getting yesterday's price for {ticker}: {e}")
    
    return None

def buy_stock(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Submit buy order
        order = api.submit_order(
            symbol=ticker,
            qty=5,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
        
        # Load existing positions
        positions_file = os.path.join(DATA_DIR, "positions.json")
        try:
            with open(positions_file, "r") as f:
                positions = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            positions = {}
        
        # Add new position
        positions[ticker] = {
            "buy-price": info.get('currentPrice'),
            "quantity": 5, 
            "buy-date": str(datetime.now().date())
        }
        
        # Save positions
        with open(positions_file, "w") as f:
            json.dump(positions, f, indent=2)
        
        print(f'Buy order placed 5 shares of {ticker}')
        
    except Exception as e:
        print(f"Error buying stock {ticker}: {e}")
    
    return 

def sell_stock():
    try:
        positions_file = os.path.join(DATA_DIR, "positions.json")
        
        # Load positions
        try:
            with open(positions_file, "r") as f:
                positions = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("No positions file found or file is empty")
            return

        stock_to_remove = []

        for ticker in positions:
            try:
                stock = yf.Ticker(ticker)
                currentPrice = stock.info.get('currentPrice')
                buy_price = positions[ticker]["buy-price"]
                target_price = buy_price * 1.10
                
                if currentPrice and currentPrice >= target_price:
                    quantity = positions[ticker]["quantity"]

                    order = api.submit_order(
                        symbol=ticker,
                        qty=quantity,
                        side='sell',
                        type='market',
                        time_in_force='gtc'
                    )

                    profit = (currentPrice - buy_price) * quantity
                    print(f'Sold {quantity} shares of {ticker} for a profit of {profit}')

                    stock_to_remove.append(ticker)
                    
            except Exception as e:
                print(f"Error processing sale for {ticker}: {e}")

        # Remove sold stocks
        for ticker in stock_to_remove:
            del positions[ticker]

        # Save updated positions
        with open(positions_file, "w") as f:
            json.dump(positions, f, indent=2)

        if not stock_to_remove:
            print("No stocks ready to sell")

    except Exception as e:
        print(f"Error in sell_stock: {e}")

    return

def portfolio_info():
    try:
        account = api.get_account()
        portfolio = {
            'portfolio-value': float(account.portfolio_value),
            'pnl': float(float(account.portfolio_value) - 100000),
        }
        
        portfolio_file = os.path.join(DATA_DIR, 'portfolio-info.json')
        with open(portfolio_file, 'w') as f:
            json.dump(portfolio, f, indent=2)
            
        print(f"Portfolio value: ${portfolio['portfolio-value']}")
        
    except Exception as e:
        print(f"Error getting portfolio info: {e}")

    return