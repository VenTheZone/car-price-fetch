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
            r'\$[\d,]+(?:\.?\d{2})?',  # Basic price format $XX,XXX.XX
            r'(?:Price|PRICE|price|Sale Price|SALE PRICE|ListPrice):\s*\$[\d,]+(?:\.?\d{2})?',
            r'[\d,]+(?:\.?\d{2})?\s*USD',
            r'salesPrice["\']:\s*["\']?\$?([\d,]+(?:\.?\d{2})?)["\']?',
            r'price["\']:\s*["\']?\$?([\d,]+(?:\.?\d{2})?)["\']?',
            r'ListPrice["\']:\s*["\']?\$?([\d,]+(?:\.?\d{2})?)["\']?'
        ]
        
        # Check structured data first
        schema_data = soup.find_all('script', type='application/ld+json')
        for schema in schema_data:
            try:
                if 'price' in schema.string.lower():
                    for pattern in price_patterns:
                        matches = re.findall(pattern, schema.string)
                        if matches:
                            return f"${matches[0]}"
            except:
                continue

        # Then check regular content
        for pattern in price_patterns:
            prices = re.findall(pattern, response.text)
            if prices:
                # Clean the price string
                price = prices[0]
                if not price.startswith('$'):
                    price = f"${price}"
                return price
        
        # Try finding specific price elements
        price_classes = ['price', 'Price', 'sale-price', 'listing-price', 'vehicle-price']
        for class_name in price_classes:
            price_elem = soup.find(class_=lambda x: x and class_name in x)
            if price_elem:
                price_text = price_elem.get_text().strip()
                if '$' in price_text:
                    return price_text
        
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
    