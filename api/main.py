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
import webscraper
import automatedinvestor as automatedinvestor
import schedule
import datetime
import pytz
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

@app.get('/positions')
def get_positions():
    path = os.path.join(DATA_DIR, "positions.json")
    if os.path.exists(path):
        return FileResponse(path, media_type="applications/json")
    return {'error': 'positions.json not found'}

@app.get('/portfolio-info')
def get_portfolio_info():
    path = os.path.join(DATA_DIR, "portfolio-info.json")
    if os.path.exists(path):
        return FileResponse(path, media_type="applications/json")
    return {'error': 'portfolio_info.json not found'}




def main():
    # Get the text from the website

    tz = pytz.timezone("Europe/Dublin")
    now = datetime.now(tz)

    text = webscraper.text_scraper()
    
    # Find sentences that contain negative words
    sentences = webscraper.find_negative_headings(text)

    
    # Write each sentence to a file
    # with open('negative_sentences.txt', 'w', encoding='utf-8') as file:
    #     for sentence in sentences:
    #         file.write(sentence)
    #Testing LLM with one heading
    # for i in range(1,len(sentences)-1):
    #     print(webscraper.research_involved_companies(sentences[i]))
    for i in range(len(sentences)):
        this = webscraper.research_involved_companies(sentences[i])
        automatedinvestor.invest(this)

schedule.every().day.at("9:00").do(main)
schedule.every().day.at("9:15").do(main)



while True:
    schedule.run_pending()
    time.sleep(15)
    