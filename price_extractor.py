import requests
from bs4 import BeautifulSoup
import re

def extract_price(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Common price patterns
        price_patterns = [
            r'\$[\d,]+(?:\.?\d{2})?',
            r'(?:Price|PRICE|price):\s*\$[\d,]+(?:\.?\d{2})?',
            r'[\d,]+(?:\.?\d{2})?\s*USD'
        ]
        
        for pattern in price_patterns:
            prices = re.findall(pattern, response.text)
            if prices:
                return prices[0]
        
        return "Price not found"
    except Exception as e:
        return f"Error extracting price: {str(e)}"

def process_results(search_results, vin):
    processed_results = []
    for url, title in search_results:
        if vin.lower() in url.lower() or vin.lower() in title.lower():
            price = extract_price(url)
            processed_results.append({
                'url': url,
                'title': title,
                'price': price
            })
    return processed_results
    