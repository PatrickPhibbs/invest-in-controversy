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
import automatedinvestor

def main():
    # Get the text from the website
    text = webscraper.text_scraper()
    
    # Find sentences that contain negative words
    sentences = webscraper.find_negative_headings(text)
    
    # Write each sentence to a file
    # with open('negative_sentences.txt', 'w', encoding='utf-8') as file:
    #     for sentence in sentences:
    #         file.write(sentence)
    #Testing LLM with one heading
    for i in range(1,len(sentences)-1):
        print(webscraper.research_involved_companies(sentences[i]))

    automatedinvestor.invest()
    