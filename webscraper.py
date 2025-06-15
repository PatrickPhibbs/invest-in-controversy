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

load_dotenv()  # This loads the .env file




    

# Function to scrape text from Yahoo Finance news
def text_scraper():
    # Wait 2 seconds to be polite to the website
    time.sleep(2)
    
    # The website we want to scrape
    url = 'https://finance.yahoo.com/topic/latest-news/'
    
    # Pretend to be a real browser so the website doesn't block us
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # Send a request to get the webpage
    response = rq.get(url, headers=headers)
    
    # Check if we're making too many requests
    if response.status_code == 429:
        print("Too many requests")
    
    # Parse the HTML from the webpage
    html = bs(response.text, 'html.parser')
    
    # Find all the headline elements (h3 tags)
    page_text = html.find_all('h3')
    
    #Converts from html to a string before returning
    text_content = ' '.join([h3.get_text(strip= True) for h3 in page_text])

    # Return the headlines (NOTE: This returns HTML elements, not text!)
    return text_content

# Function to find headlines with negative/bad news words
def find_negative_headings(text):
    # List of words that indicate bad news or problems
    controversy_keywords = [
        # Direct controversy/scandal indicators
        "lawsuit",      # Legal trouble
        "bankruptcy",   # Company going broke
        "crisis",       # Emergency situation
        "scandal",      # Bad behavior exposed
        "investigation", # Being looked into for wrongdoing
        "fraud",        # Cheating/stealing
        "controversy",  # Public disagreement/argument
        
        # Financial distress signals
        "plummets",     # Falls very fast
        "plunges",      # Drops suddenly
        "falls",        # Goes down
        "fell",         # Went down (past tense)
        "drops",        # Decreases
        "dropped",      # Decreased (past tense)
        "tumbles",      # Falls quickly
        "weak results",         # Poor performance
        "underwhelming results", # Disappointing performance
        "poor results",         # Bad performance
        "missed estimates",     # Did worse than expected
        "withdrawn outlook",    # Company took back their predictions
        "guidance cut",         # Lowered future predictions
        "layoffs",             # Firing employees
        "restructuring",       # Reorganizing (usually means cuts)
        "downsizing",          # Making company smaller
        
        # Market warning words
        "risks",        # Dangers
        "concerns",     # Worries
        "worries",      # Concerns
        "declines",     # Goes down
        "declining",    # Going down
        "tariffs",      # Trade taxes (usually bad for business)
        "stressed",     # Under pressure
        "volatile",     # Unpredictable/unstable
        "uncertainty",  # Not knowing what will happen
        "warning",      # Alert about problems
        "caution",      # Be careful
        "alert",        # Warning
        
        # Performance indicators
        "loss",                 # Losing money
        "losses",              # Lost money
        "deficit",             # Shortage/not enough
        "shortfall",           # Coming up short
        "disappointing",       # Let down expectations
        "below expectations",  # Worse than hoped
        "underperformed",      # Did worse than expected
        "struggled",           # Had difficulty
        "challenges",          # Problems to solve
        "difficulties",        # Problems
        "problems",            # Issues
        "issues",              # Problems
        "trouble",             # Problems
        "troubled"             # Having problems
    ]
    
    # Try to split the text into sentences 
    sentences = re.split(r'[.!?]+', text)
    
    
    # List to store sentences that contain negative words
    matching_sentences = []
    
    # Look through each sentence
    for sentence in sentences:
        # Remove extra spaces (NOTE: This doesn't actually change the sentence!)
        sentence.strip()
        
        # Skip empty sentences
        if not sentence:
            continue
            
        # Convert sentence to lowercase for easier matching
        sentence_lower = sentence.lower()
        
        # Check if any negative word is in this sentence
        for keyword in controversy_keywords:
            if keyword in sentence_lower:
                # Found a negative word! Add this sentence to our list
                matching_sentences.append(sentence_lower)
                # Stop looking for more keywords in this sentence
                break
    
    # Return all the negative sentences we found
    return matching_sentences

def research_involved_companies(headline):
    # This prompts the gemini llm with the inputted headline in order to get a response in the form of a list of companies that may be negatively affected.
    genai.configure(api_key=os.getenv('GOOGLEAI_TOKEN'))
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    Analyze this headline find out what companies would be affected negatively by whatever has happened in this specific news article

    Headline = "{headline}"


    Don't add any fluff text literally just the company stock tickers in a list.

    Focus on major public companies only.
    Dont add any notes, the only text I want outputted is the company tickers.
    """

    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.3,
            max_output_tokens=500,
        )
    )
        
        
        

    return response.text.strip()

def parse_company_name():
    return
# Run the main function
main()