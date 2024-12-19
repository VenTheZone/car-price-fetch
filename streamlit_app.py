import streamlit as st
import requests
from bs4 import BeautifulSoup


def get_car_prices(vin):
    urls = [
        f'https://www.cars.com/search/?q={vin}',
        f'https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=carGurusHomePage&listType=&entitySelectingHelper.selectedEntity=cars.com&zip={vin}',
        f'https://www.autotrader.com/cars-for-sale/all-cars?searchRadius=0&q={vin}',
        f'https://www.capitalone.com/cars-for-sale/searchresults/?query={vin}',
    ]
    prices = []
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            soup = BeautifulSoup(response.text, 'html.parser')
            price_elements = soup.select('.price')
            for price in price_elements:
                prices.append(price.get_text(strip=True))
        except requests.exceptions.RequestException as e:
            st.error(f'Error fetching data from {url}: {e}')  # Log the error in Streamlit
        except Exception as e:
            st.error(f'An unexpected error occurred: {e}')
    return prices


st.title("Car Price Comparison")
vin_input = st.text_input("Enter VIN:")
if vin_input:
    prices = get_car_prices(vin_input)
    if prices:
        st.write("Prices found:", prices)
    else:
        st.write("No prices found.")