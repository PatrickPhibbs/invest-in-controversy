# Import libraries we need
import pandas as pd  # For data handling (not used in this code)
import requests as rq  # For making web requests
from bs4 import BeautifulSoup as bs  # For parsing HTML
import schedule  # For scheduling tasks (not used in this code)
import time  # For adding delays
import re  # For text pattern matching
import os
from dotenv import load_dotenv
import google.generativeai as genai
import yfinance as yf
import alpaca_trade_api as tradeapi
from datetime import datetime
import yfinance as yf
import json

load_dotenv()  
api = tradeapi.REST(
        os.getenv('APCA_API_KEY_ID'), 
        os.getenv('APCA_API_SECRET_KEY'), 
        'https://paper-api.alpaca.markets', 
        api_version='v2'
    )

def invest(unparsed_tickers):
    account = api.get_account()
    parsed_tickers = parse_tickers_from_string(unparsed_tickers)
    #temporary function call just to calculate the past prices of 1 ticker
    int = calculate_dip(parsed_tickers[len(parsed_tickers)-1])
    print('This is the price of '+parsed_tickers[len(parsed_tickers)-1]+': '+str(int))
    sell_stock()
    
    return

def parse_tickers_from_string(text):
    pattern = r'\$?([A-Z]{1,5})\b'
    tickers = re.findall(pattern, text)
    return list(set(tickers))

def calculate_dip(ticker):
    #
    #
    stock = yf.Ticker(ticker)
    info = stock.info
    current_price =  info.get('currentPrice')
    if get_price_yesterday(ticker)!=None:
        if (current_price <= (get_price_yesterday(ticker)*0.99)):
            buy_stock(ticker)
        else:
            print(f'{ticker} not bought')

    print('This is the price now: ' + str(current_price) + ' and this is the price three days ago: '+ str(get_price_yesterday(ticker)))

    return

def get_price_yesterday(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period='5d')

    if not hist.empty:
        last_close = hist['Close'].iloc[-3]
        return round(last_close, 2)
    
    return None

def buy_stock(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    order = api.submit_order(
        symbol=ticker,
        qty=5,
        side='buy',
        type='market',
        time_in_force='gtc'
    )
    try:
        with open("positions.json", "r") as f:
            positions = json.load(f)
    except FileNotFoundError:
        positions = {}
    positions[ticker] = {
        "buy-price": info.get('currentPrice'),
        "quantity": 5, 
        "buy-date": str(datetime.now().date())
    }
    with open("positions.json","w") as f:
        json.dump(positions,f)
    print(f'Buy order placed 5 shares of {ticker}')
    return 

def sell_stock():
    with open("positions.json", "r") as f:
        positions = json.load(f)

    stock_to_remove = []

    for ticker in positions:
        stock = yf.Ticker(ticker)
        currentPrice = stock.info.get('currentPrice')
        buy_price = positions[ticker]["buy-price"]
        target_price = buy_price*1.10
        
        if currentPrice >= target_price:
            quantity = positions[ticker]["quantity"]

            order = api.submit_order(
                symbol = ticker,
                qty = quantity,
                side = 'sell',
                type = 'market',
                time_in_force = 'gtc'
            )

            profit = (currentPrice - buy_price) * quantity
            print(f'Sold {quantity} shares of {ticker} for a profit of {profit}')

            stock_to_remove.append(ticker)

    for ticker in stock_to_remove:
        del positions[ticker]

    with open("positions.json","w") as f:
        json.dump(positions, f)

    if not stock_to_remove:
        print("No stocks ready to sell")


    return


