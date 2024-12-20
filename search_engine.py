import requests
import streamlit as st

def search_brave(vin):
    brave_url = f"https://api.search.brave.com/res/v1/web/search"
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
        'X-Subscription-Token': 'YOUR_BRAVE_API_KEY'
    }
    
    query = f'site:capitalone.com OR site:autotrader.com OR site:cargurus.com OR site:cars.com "{vin}" "price"'
    
    params = {
        'q': query,
        'count': 10
    }
    
    try:
        response = requests.get(brave_url, headers=headers, params=params)
        if response.status_code == 200:
            results = response.json()
            return [(item['url'], item['title']) for item in results.get('web', {}).get('results', [])]
    except Exception as e:
        st.error(f"Brave Search Error: {str(e)}")
    return []

def search_duckduckgo(vin):
    duckduckgo_url = "https://api.duckduckgo.com/"
    
    query = f'site:capitalone.com OR site:autotrader.com OR site:cargurus.com OR site:cars.com "{vin}" "price"'
    
    params = {
        'q': query,
        'format': 'json',
        'no_html': 1,
        'no_redirect': 1
    }
    
    try:
        response = requests.get(duckduckgo_url, params=params)
        if response.status_code == 200:
            results = response.json()
            return [(result['link'], result['title']) for result in results.get('Results', [])]
    except Exception as e:
        st.error(f"DuckDuckGo Search Error: {str(e)}")
    return []
    