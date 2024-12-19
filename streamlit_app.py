import streamlit as st
import requests
from bs4 import BeautifulSoup

def get_car_prices(vin):
    # Define the list of URLs to fetch data from
    urls = [
        f'https://www.cars.com/search/?q={vin}',
        f'https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=carGurusHomePage&listType=&entitySelectingHelper.selectedEntity=cars.com&zip={vin}',
        f'https://www.autotrader.com/cars-for-sale/all-cars?searchRadius=0&q={vin}',
        f'https://www.capitalone.com/cars-for-sale/searchresults/?query={vin}',
    ]
    prices = []
    # Loop through each URL and fetch prices
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Modify this selector to match the site's price element
        price_elements = soup.select('.price')  # Update this selector if necessary
        # Collect the prices found
        for price in price_elements:
            prices.append(price.get_text(strip=True))
    return prices

# Streamlit UI elements
st.title("Car Price Comparison")
vin_input = st.text_input("Enter VIN:")
if vin_input:
    prices = get_car_prices(vin_input)
    if prices:
        st.write("Prices found:", prices)
    else:
        st.write("No prices found.")