import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to scrape car data for a given VIN
def scrape_car_data(vin):
    sites = [
        ("cars.com", f"https://www.cars.com/shopping/results/?stock_type=all&vin={vin}"),
        ("cargurus.com", f"https://www.cargurus.com/Cars/link/{vin}"),
        ("autotrader.com", f"https://www.autotrader.com/cars-for-sale/vehicledetails/{vin}"),
        ("capitalone.com", f"https://www.capitalone.com/cars/{vin}")
    ]

    results = []

    for site_name, url in sites:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            soup = BeautifulSoup(response.content, 'html.parser')
            price = soup.find('span', {'class': 'price'})
            price_value = price.get_text(strip=True) if price else 'Price not found'
        except requests.exceptions.RequestException as e:
            price_value = f'Error retrieving data from {site_name}: {e}'
        except Exception as e:
            price_value = f'Error parsing data from {site_name}: {e}'

        results.append({
            'site': site_name,
            'price': price_value
        })

    return results

# Streamlit App
st.title("Car Price Comparison by VIN")
vin_input = st.text_input("Enter VIN number:")

if vin_input:
    with st.spinner("Fetching data..."):
        car_prices = scrape_car_data(vin_input)
        st.write("Price Comparison Results:")
        for car in car_prices:
            st.write(f"{car['site']}: {car['price']}")