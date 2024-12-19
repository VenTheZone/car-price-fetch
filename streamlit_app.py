import requests
from bs4 import BeautifulSoup
import streamlit as st
import re

def is_valid_vin(vin):
    return bool(re.match(r'^[A-HJ-NPR-Z0-9]{17}$', vin))

st.title('VIN Price Scraper')
vin_input = st.text_input('Enter VIN:')

if vin_input:
    if is_valid_vin(vin_input):
        st.write('Fetching results...')
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        query = f'{vin_input} site:cars.com OR site:cargurus.com OR site:autotrader.com OR site:capitalone.com/cars/'
        search_url = f'https://duckduckgo.com/html/?q={query}'

        try:
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            results = []
            for link in soup.find_all('a', class_='result__a'):
                href = link.get('href')
                title = link.get_text()
                results.append({'title': title, 'url': href})

            if results:
                st.write('### Results')
                for result in results:
                    st.write(f"[{result['title']}]({result['url']})")
            else:
                st.write('No results found.')

        except requests.exceptions.RequestException as e:
            st.error(f'An error occurred: {e}')
    else:
        st.error('Invalid VIN. Please enter a 17-character VIN containing only letters and numbers.')