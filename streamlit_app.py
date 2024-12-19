pip install streamlit requests pandas

streamlit run car_comparison.py


import streamlit as st
import requests
import pandas as pd
import time
import json
from concurrent.futures import ThreadPoolExecutor

# Configure page settings
st.set_page_config(
    page_title="Car Comparison Tool",
    page_icon="",
    layout="wide"
)

# Custom CSS
st.markdown("""
    
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border-radius: 5px;
    }
    .stAlert {
        padding: 20px;
        border-radius: 10px;
    }
    .car-image {
        width: 100%;
        max-width: 300px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
""", unsafe_allow_html=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

def fetch_autotrader(search_term):
    """Fetch data from AutoTrader API"""
    try:
        url = f"https://www.autotrader.com/rest/searchresults/base?query={search_term}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = []
            listings = data.get('listings', [])[:5]
            for listing in listings:
                results.append({
                    'source': 'AutoTrader',
                    'title': listing.get('title', ''),
                    'price': listing.get('price', {}).get('display', 'N/A'),
                    'image_url': listing.get('images', [{}])[0].get('src', None)
                })
            return results
        return []
    except Exception as e:
        st.error(f"Error fetching from AutoTrader: {str(e)}")
        return []

def fetch_cargurus(search_term):
    """Fetch data from CarGurus API"""
    try:
        url = f"https://www.cargurus.com/Cars/api/search-results?searchTerm={search_term}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = []
            listings = data.get('listings', [])[:5]
            for listing in listings:
                results.append({
                    'source': 'CarGurus',
                    'title': listing.get('title', ''),
                    'price': listing.get('price', {}).get('formatted', 'N/A'),
                    'image_url': listing.get('image', {}).get('url', None)
                })
            return results
        return []
    except Exception as e:
        st.error(f"Error fetching from CarGurus: {str(e)}")
        return []

def fetch_cars_com(search_term):
    """Fetch data from Cars.com API"""
    try:
        url = f"https://www.cars.com/api/v1/search?q={search_term}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = []
            listings = data.get('listings', [])[:5]
            for listing in listings:
                results.append({
                    'source': 'Cars.com',
                    'title': listing.get('title', ''),
                    'price': listing.get('price', {}).get('display', 'N/A'),
                    'image_url': listing.get('primary_photo', {}).get('url', None)
                })
            return results
        return []
    except Exception as e:
        st.error(f"Error fetching from Cars.com: {str(e)}")
        return []

def main():
    st.title(" Multi-Dealer Car Comparison Tool")
    
    # Input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_type = st.radio(
            "Search by:",
            ["VIN", "Car Model"],
            horizontal=True
        )
        
        if search_type == "VIN":
            search_term = st.text_input("Enter VIN number:", placeholder="e.g., 1HGCM82633A123456")
        else:
            search_term = st.text_input("Enter car model:", placeholder="e.g., Honda Civic 2022")

    with col2:
        st.markdown("### Search Options")
        include_autotrader = st.checkbox("Include AutoTrader", value=True)
        include_cargurus = st.checkbox("Include CarGurus", value=True)
        include_cars_com = st.checkbox("Include Cars.com", value=True)

    if st.button("Search Cars"):
        if not search_term:
            st.warning("Please enter a search term first!")
            return

        with st.spinner("Searching across dealers..."):
            # Create a progress bar
            progress_bar = st.progress(0)
            
            # Initialize results list
            all_results = []
            
            # Use ThreadPoolExecutor for parallel requests
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = []
                
                if include_autotrader:
                    futures.append(executor.submit(fetch_autotrader, search_term))
                if include_cargurus:
                    futures.append(executor.submit(fetch_cargurus, search_term))
                if include_cars_com:
                    futures.append(executor.submit(fetch_cars_com, search_term))
                
                # Update progress as results come in
                for i, future in enumerate(futures):
                    progress = (i + 1) / len(futures)
                    progress_bar.progress(progress)
                    results = future.result()
                    all_results.extend(results)
                    time.sleep(0.5)  # Small delay for visual effect

            # Convert results to DataFrame
            if all_results:
                df = pd.DataFrame(all_results)
                
                # Display results in a grid layout
                for i in range(0, len(df), 3):
                    cols = st.columns(3)
                    for j in range(3):
                        if i + j < len(df):
                            with cols[j]:
                                st.subheader(df.iloc[i + j]['source'])
                                if df.iloc[i + j]['image_url']:
                                    st.image(df.iloc[i + j]['image_url'], 
                                           caption=df.iloc[i + j]['title'],
                                           use_column_width=True)
                                st.write(f"**{df.iloc[i + j]['title']}**")
                                st.write(f"Price: {df.iloc[i + j]['price']}")

                # Add download button
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Results",
                    data=csv,
                    file_name="car_comparison_results.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No results found. Try modifying your search terms.")

if __name__ == "__main__":
    main()



import streamlit as st
import requests
import pandas as pd
import time
import json
from concurrent.futures import ThreadPoolExecutor

# Configure page settings
st.set_page_config(
    page_title="Car Comparison Tool",
    page_icon="",
    layout="wide"
)

# Custom CSS
st.markdown("""
    
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border-radius: 5px;
    }
    .stAlert {
        padding: 20px;
        border-radius: 10px;
    }
    .car-image {
        width: 100%;
        max-width: 300px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
""", unsafe_allow_html=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

def fetch_autotrader(search_term):
    """Fetch data from AutoTrader API"""
    try:
        url = f"https://www.autotrader.com/rest/searchresults/base?query={search_term}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = []
            listings = data.get('listings', [])[:5]
            for listing in listings:
                results.append({
                    'source': 'AutoTrader',
                    'title': listing.get('title', ''),
                    'price': listing.get('price', {}).get('display', 'N/A'),
                    'image_url': listing.get('images', [{}])[0].get('src', None)
                })
            return results
        return []
    except Exception as e:
        st.error(f"Error fetching from AutoTrader: {str(e)}")
        return []

def fetch_cargurus(search_term):
    """Fetch data from CarGurus API"""
    try:
        url = f"https://www.cargurus.com/Cars/api/search-results?searchTerm={search_term}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = []
            listings = data.get('listings', [])[:5]
            for listing in listings:
                results.append({
                    'source': 'CarGurus',
                    'title': listing.get('title', ''),
                    'price': listing.get('price', {}).get('formatted', 'N/A'),
                    'image_url': listing.get('image', {}).get('url', None)
                })
            return results
        return []
    except Exception as e:
        st.error(f"Error fetching from CarGurus: {str(e)}")
        return []

def fetch_cars_com(search_term):
    """Fetch data from Cars.com API"""
    try:
        url = f"https://www.cars.com/api/v1/search?q={search_term}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = []
            listings = data.get('listings', [])[:5]
            for listing in listings:
                results.append({
                    'source': 'Cars.com',
                    'title': listing.get('title', ''),
                    'price': listing.get('price', {}).get('display', 'N/A'),
                    'image_url': listing.get('primary_photo', {}).get('url', None)
                })
            return results
        return []
    except Exception as e:
        st.error(f"Error fetching from Cars.com: {str(e)}")
        return []

def main():
    st.title(" Multi-Dealer Car Comparison Tool")
    
    # Input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_type = st.radio(
            "Search by:",
            ["VIN", "Car Model"],
            horizontal=True
        )
        
        if search_type == "VIN":
            search_term = st.text_input("Enter VIN number:", placeholder="e.g., 1HGCM82633A123456")
        else:
            search_term = st.text_input("Enter car model:", placeholder="e.g., Honda Civic 2022")

    with col2:
        st.markdown("### Search Options")
        include_autotrader = st.checkbox("Include AutoTrader", value=True)
        include_cargurus = st.checkbox("Include CarGurus", value=True)
        include_cars_com = st.checkbox("Include Cars.com", value=True)

    if st.button("Search Cars"):
        if not search_term:
            st.warning("Please enter a search term first!")
            return

        with st.spinner("Searching across dealers..."):
            # Create a progress bar
            progress_bar = st.progress(0)
            
            # Initialize results list
            all_results = []
            
            # Use ThreadPoolExecutor for parallel requests
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = []
                
                if include_autotrader:
                    futures.append(executor.submit(fetch_autotrader, search_term))
                if include_cargurus:
                    futures.append(executor.submit(fetch_cargurus, search_term))
                if include_cars_com:
                    futures.append(executor.submit(fetch_cars_com, search_term))
                
                # Update progress as results come in
                for i, future in enumerate(futures):
                    progress = (i + 1) / len(futures)
                    progress_bar.progress(progress)
                    results = future.result()
                    all_results.extend(results)
                    time.sleep(0.5)  # Small delay for visual effect

            # Convert results to DataFrame
            if all_results:
                df = pd.DataFrame(all_results)
                
                # Display results in a grid layout
                for i in range(0, len(df), 3):
                    cols = st.columns(3)
                    for j in range(3):
                        if i + j < len(df):
                            with cols[j]:
                                st.subheader(df.iloc[i + j]['source'])
                                if df.iloc[i + j]['image_url']:
                                    st.image(df.iloc[i + j]['image_url'], 
                                           caption=df.iloc[i + j]['title'],
                                           use_column_width=True)
                                st.write(f"**{df.iloc[i + j]['title']}**")
                                st.write(f"Price: {df.iloc[i + j]['price']}")

                # Add download button
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Results",
                    data=csv,
                    file_name="car_comparison_results.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No results found. Try modifying your search terms.")

if __name__ == "__main__":
    main()


