import streamlit as st
import requests


def get_car_prices(vin):
    api_url = f'https://example.com/api/cars?vin={vin}'  # Hypothetical API endpoint
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        prices = data.get('prices', [])  # Assuming the API returns a JSON structure with a 'prices' key
    except requests.exceptions.RequestException as e:
        st.error(f'Error fetching data: {e}')  # Log the error in Streamlit
        prices = []  # Ensure prices is an empty list in case of error
    return prices


st.title("Car Price Comparison")
vin_input = st.text_input("Enter VIN:")
if vin_input:
    prices = get_car_prices(vin_input)
    if prices:
        st.write("Prices found:", prices)
    else:
        st.write("No prices found.")