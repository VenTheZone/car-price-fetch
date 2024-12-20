import requests
import streamlit as st
from bs4 import BeautifulSoup

def search_brave(vin):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.1312.60 Safari/537.17'
    }
    
    query = f'site:capitalone.com OR site:autotrader.com OR site:cargurus.com OR site:cars.com "{vin}" "price"'
    brave_url = f"https://search.brave.com/api/search?q={query}&source=web"
    
    try:
        response = requests.get(brave_url, headers=headers)
        if response.status_code == 200:
            results = response.json()
            return [(item['url'], item['title']) for item in results.get('results', [])]
    except Exception as e:
        st.error(f"Brave Search Error: {str(e)}")
    return []

def search_duckduckgo(vin):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0",
    }
    
    query = f'site:capitalone.com OR site:autotrader.com OR site:cargurus.com OR site:cars.com "{vin}" "price"'
    
    try:
        # Use the HTML endpoint instead of the API
        response = requests.get(f'https://duckduckgo.com/html/?q={query}', headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all("a", class_="result__url", href=True)
            
            # Extract URLs and titles from the results
            search_results = []
            for link in results:
                title = link.get_text() or "No Title"
                url = link['href']
                search_results.append((url, title))
            
            return search_results
    except Exception as e:
        st.error(f"DuckDuckGo Search Error: {str(e)}")
    return []
    