import requests
import streamlit as st
from bs4 import BeautifulSoup

def search_brave(vin):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.1312.60 Safari/537.17'
    }
    
    search_sites = [
        'site:capitalone.com',
        'site:autotrader.com',
        'site:cargurus.com', 
        'site:cars.com'
    ]
    
    all_results = []
    for site in search_sites:
        query = f'{site} inurl:{vin}'
        brave_url = f"https://search.brave.com/api/search?q={query}&source=web"
        
        try:
            response = requests.get(brave_url, headers=headers)
            if response.status_code == 200:
                results = response.json()
                all_results.extend([(item['url'], item['title']) for item in results.get('results', [])])
        except Exception as e:
            st.error(f"Brave Search Error ({site}): {str(e)}")
    
    return all_results

def search_duckduckgo(vin):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0",
    }
    
    search_sites = [
        'site:capitalone.com',
        'site:autotrader.com',
        'site:cargurus.com', 
        'site:cars.com'
    ]
    
    all_results = []
    for site in search_sites:
        query = f'{site} inurl:{vin}'
        
        try:
            response = requests.get(f'https://duckduckgo.com/html/?q={query}', headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = soup.find_all("a", class_="result__url", href=True)
                
                for link in results:
                    title = link.get_text() or "No Title"
                    url = link['href']
                    all_results.append((url, title))
                    
        except Exception as e:
            st.error(f"DuckDuckGo Search Error ({site}): {str(e)}")
            
    return all_results
    