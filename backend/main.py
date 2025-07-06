# Import libraries we need
import pandas as pd  # For data handling (not used in this code)
import httpx as rq
from bs4 import BeautifulSoup as bs  # For parsing HTML
import schedule  # For scheduling tasks
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
import threading
import json
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# Global variable to track if scheduler is running
scheduler_running = False

def main_trading_logic():
    """Main trading logic function"""
    try:
        # Get the text from the website 
        tz = pytz.timezone("Europe/Dublin")
        now = datetime.datetime.now(tz)
        
        print(f"Running trader at {now}")
        
        text = webscraper.text_scraper()
        
        # Find sentences that contain negative words
        sentences = webscraper.find_negative_headings(text)
        
        # Process each sentence
        for i in range(len(sentences)):
            this = webscraper.research_involved_companies(sentences[i])
            automatedinvestor.invest(this)
            
        print("Trading logic completed successfully")
        
    except Exception as e:
        print(f"Error in trading logic: {e}")

def run_scheduler():
    """Function to run the scheduler in background"""
    global scheduler_running
    
    # Schedule the tasks
    schedule.every().day.at("09:00").do(main_trading_logic)
    schedule.every().day.at("09:15").do(main_trading_logic)
    
    scheduler_running = True
    print("Scheduler started - tasks scheduled for 9:00 AM and 9:15 AM Dublin time")
    
    while scheduler_running:
        schedule.run_pending()
        time.sleep(60)  # Check every minute instead of 15 seconds

@app.on_event("startup")
async def startup_event():
    """Start the scheduler when the app starts"""
    # Start scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

@app.get('/')
def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "message": "Trading bot API is active",
        "scheduler_running": scheduler_running
    }

@app.get('/positions')
def get_positions():
    """Get current positions"""
    path = os.path.join(DATA_DIR, "positions.json")
    if os.path.exists(path):
        return FileResponse(path, media_type="application/json")
    return {'error': 'positions.json not found'}

@app.get('/portfolio-info')
def get_portfolio_info():
    """Get portfolio information"""
    path = os.path.join(DATA_DIR, "portfolio-info.json")
    if os.path.exists(path):
        return FileResponse(path, media_type="application/json")
    return {'error': 'portfolio_info.json not found'}

@app.post('/run-trader')
def run_trader_manual(background_tasks: BackgroundTasks):
    """Manually trigger the trading logic"""
    background_tasks.add_task(main_trading_logic)
    return {"message": "Trading logic started in background"}

@app.get('/status')
def get_status():
    """Get current status of the application"""
    tz = pytz.timezone("Europe/Dublin")
    now = datetime.datetime.now(tz)
    
    return {
        "current_time": now.isoformat(),
        "scheduler_running": scheduler_running,
        "next_runs": [
            "9:00 Dublin time",
            "9:15 Dublin time"
        ]
    }

@app.post('/positions')
def update_positions(positions: dict):
    """Update positions data"""
    try:
        path = os.path.join(DATA_DIR, "positions.json")
        with open(path, 'w') as f:
            json.dump(positions, f, indent=2)
        return {"message": "Positions updated successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.post('/portfolio')
def update_portfolio(portfolio: dict):
    """Update portfolio data"""
    try:
        path = os.path.join(DATA_DIR, "portfolio-info.json")
        with open(path, 'w') as f:
            json.dump(portfolio, f, indent=2)
        return {"message": "Portfolio updated successfully"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)