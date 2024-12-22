from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import streamlit as st

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def search_perplexity(vin):
    driver = setup_driver()
    all_results = []
    
    try:
        search_query = f"""Create an Excel sheet that lists the price of the vehicle identified by {vin} from the following websites:

        site:capitalone.com
        site:autotrader.com
        site:cargurus.com
        site:cars.com

        The sheet should include:
        1. Website name
        2. Price
        3. Weblink to the listing"""

        url = f"https://www.perplexity.ai/?q={search_query}"
        driver.get(url)
        time.sleep(5)

        results = driver.find_elements(By.CSS_SELECTOR, "a")
        for result in results[:5]:
            title = result.text
            link = result.get_attribute("href")
            if link and vin.lower() in link.lower():
                all_results.append((link, title))

    except Exception as e:
        st.error(f"Perplexity Search Error: {str(e)}")
    
    finally:
        driver.quit()
    
    return all_results
    