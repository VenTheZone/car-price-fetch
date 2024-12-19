import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
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
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .user-message {
        background-color: #2c3e50;
    }
    .bot-message {
        background-color: #34495e;
    }
    
""", unsafe_allow_html=True)

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_autotrader(search_term, driver):
    """Scrape data from AutoTrader"""
    try:
        url = f"https://www.autotrader.com/cars-for-sale/all-cars/{search_term}"
        driver.get(url)
        time.sleep(3)  # Allow page to load
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        listings = soup.find_all('div', {'data-test': 'listing-card'})[:5]
        
        results = []
        for listing in listings:
            title = listing.find('h2').text if listing.find('h2') else 'N/A'
            price = listing.find('span', {'data-test': 'price'}).text if listing.find('span', {'data-test': 'price'}) else 'N/A'
            image = listing.find('img')['src'] if listing.find('img') else None
            
            results.append({
                'source': 'AutoTrader',
                'title': title,
                'price': price,
                'image_url': image
            })
        return results
    except Exception as e:
        st.error(f"Error scraping AutoTrader: {str(e)}")
        return []

def chat_message(message, is_user=False):
    """Display a chat message"""
    className = "user-message" if is_user else "bot-message"
    st.markdown(f'{message}', unsafe_allow_html=True)

def main():
    st.title("")
    
    # Chat section
    st.sidebar.title("Chat Assistant")
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        chat_message(message['text'], message['is_user'])

    # Chat input
    user_input = st.sidebar.text_input("Ask me anything about cars:", key="user_input")
    if st.sidebar.button("Send"):
        if user_input:
            # Add user message to chat
            st.session_state.messages.append({'text': user_input, 'is_user': True})
            # Simple bot response
            response = f"I understand you're asking about {user_input}. I'm here to help with car-related questions!"
            st.session_state.messages.append({'text': response, 'is_user': False})
            st.experimental_rerun()

    # Main search interface
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

    if st.button("Search Cars"):
        if not search_term:
            st.warning("Please enter a search term first!")
            return

        with st.spinner("Scraping car data..."):
            driver = setup_driver()
            try:
                results = scrape_autotrader(search_term, driver)
                
                if results:
                    df = pd.DataFrame(results)
                    
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
            finally:
                driver.quit()

if __name__ == "__main__":
    main()



import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
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
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .user-message {
        background-color: #2c3e50;
    }
    .bot-message {
        background-color: #34495e;
    }
    
""", unsafe_allow_html=True)

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_autotrader(search_term, driver):
    """Scrape data from AutoTrader"""
    try:
        url = f"https://www.autotrader.com/cars-for-sale/all-cars/{search_term}"
        driver.get(url)
        time.sleep(3)  # Allow page to load
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        listings = soup.find_all('div', {'data-test': 'listing-card'})[:5]
        
        results = []
        for listing in listings:
            title = listing.find('h2').text if listing.find('h2') else 'N/A'
            price = listing.find('span', {'data-test': 'price'}).text if listing.find('span', {'data-test': 'price'}) else 'N/A'
            image = listing.find('img')['src'] if listing.find('img') else None
            
            results.append({
                'source': 'AutoTrader',
                'title': title,
                'price': price,
                'image_url': image
            })
        return results
    except Exception as e:
        st.error(f"Error scraping AutoTrader: {str(e)}")
        return []

def chat_message(message, is_user=False):
    """Display a chat message"""
    className = "user-message" if is_user else "bot-message"
    st.markdown(f'{message}', unsafe_allow_html=True)

def main():
    st.title("")
    
    # Chat section
    st.sidebar.title("Chat Assistant")
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        chat_message(message['text'], message['is_user'])

    # Chat input
    user_input = st.sidebar.text_input("Ask me anything about cars:", key="user_input")
    if st.sidebar.button("Send"):
        if user_input:
            # Add user message to chat
            st.session_state.messages.append({'text': user_input, 'is_user': True})
            # Simple bot response
            response = f"I understand you're asking about {user_input}. I'm here to help with car-related questions!"
            st.session_state.messages.append({'text': response, 'is_user': False})
            st.experimental_rerun()

    # Main search interface
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

    if st.button("Search Cars"):
        if not search_term:
            st.warning("Please enter a search term first!")
            return

        with st.spinner("Scraping car data..."):
            driver = setup_driver()
            try:
                results = scrape_autotrader(search_term, driver)
                
                if results:
                    df = pd.DataFrame(results)
                    
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
            finally:
                driver.quit()

if __name__ == "__main__":
    main()


