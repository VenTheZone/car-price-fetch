import requests
from bs4 import BeautifulSoup
import streamlit as st

st.title('VIN Price Scraper')
vin_input = st.text_input('Enter VIN:')

if vin_input:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    query = vin_input + ' site:cars.com OR site:cargurus.com OR site:autotrader.com OR site:capitalone.com/cars/'
    search_url = f'https://duckduckgo.com/html/?q={query}'

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for link in soup.find_all('a', class_='result__a'):
        url = link.get('href')
        title = link.get_text()
        results.append({'title': title, 'url': url})

    st.write('### Results')
    for result in results:
        st.write(f"[{result['title']}]({result['url']})")