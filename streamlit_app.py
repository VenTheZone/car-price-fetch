import streamlit as st
from search_engines import search_brave, search_duckduckgo
from price_extractor import process_results
import concurrent.futures
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import BytesIO
import datetime

def search_brave(vin):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.1312.60 Safari/537.17'
    }
    
    search_sites = [
        'site:capitalone.com',
        'site:autotrader.com',
        'site:cargurus.com', 
        'site:cars.com'
    ]
    
    all_results = []
    for site in search_sites:
        query = f'{site} inurl:{vin}'
        brave_url = f"https://search.brave.com/api/search?q={query}&source=web"
        
        try:
            response = requests.get(brave_url, headers=headers)
            if response.status_code == 200:
                results = response.json()
                all_results.extend([(item['url'], item['title']) for item in results.get('results', [])])
        except Exception as e:
            st.error(f"Brave Search Error ({site}): {str(e)}")
    
    return all_results

def search_duckduckgo(vin):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0",
    }
    
    search_sites = [
        'site:capitalone.com',
        'site:autotrader.com',
        'site:cargurus.com', 
        'site:cars.com'
    ]
    
    all_results = []
    for site in search_sites:
        query = f'{site} inurl:{vin}'
        
        try:
            response = requests.get(f'https://duckduckgo.com/html/?q={query}', headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = soup.find_all("a", class_="result__url", href=True)
                
                for link in results:
                    title = link.get_text() or "No Title"
                    url = link['href']
                    all_results.append((url, title))
                    
        except Exception as e:
            st.error(f"DuckDuckGo Search Error ({site}): {str(e)}")
            
    return all_results


def main():
    st.title("Multi-Engine VIN Price Searcher")
    st.write("Enter a VIN number to search across multiple automotive websites")
    
    vin_input = st.text_input("VIN Number:", "")
    
    if st.button("Search"):
        if vin_input:
            with st.spinner("Searching..."):
                search_sites = ['Capital One', 'AutoTrader', 'CarGurus', 'Cars.com']
                progress_text = st.empty()
                progress_bar = st.progress(0)
                
                # Search using both engines
                progress_text.text("Searching Brave...")
                brave_results = search_brave(vin_input)
                progress_bar.progress(50)
                
                progress_text.text("Searching DuckDuckGo...")
                ddg_results = search_duckduckgo(vin_input)
                progress_bar.progress(100)
                
                progress_text.empty()
                
                # Combine and process results
                all_results = list(set(brave_results + ddg_results))  # Remove duplicates
                
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    processed_results = list(executor.map(
                        lambda x: process_results([x], vin_input),
                        all_results
                    ))
                
                # Flatten results
                processed_results = [item for sublist in processed_results for item in sublist]
                
                # Display results
                if processed_results:
                    st.success(f"Found {len(processed_results)} results containing VIN: {vin_input}")
                    
                    # Create DataFrame for display and export
                    df = pd.DataFrame(processed_results)
                    df = df[['title', 'price', 'url']]  # Reorder columns
                    df.columns = ['Title', 'Price', 'URL']  # Rename columns
                    
                    # Display as a styled table
                    st.dataframe(
                        df.style.set_properties(**{
                            'background-color': 'rgba(26, 26, 26, 0.7)',
                            'color': '#00ff9f'
                        })
                    )
                    
                    # Create Excel file
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df.to_excel(writer, sheet_name='VIN Search Results', index=False)
                        
                        # Auto-adjust columns width
                        worksheet = writer.sheets['VIN Search Results']
                        for idx, col in enumerate(df.columns):
                            max_length = max(
                                df[col].astype(str).apply(len).max(),
                                len(col)
                            )
                            worksheet.column_dimensions[chr(65 + idx)].width = max_length + 2
                    
                    # Offer download button
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    excel_file = output.getvalue()
                    st.download_button(
                        label="📥 Download Excel Report",
                        data=excel_file,
                        file_name=f'vin_search_results_{timestamp}.xlsx',
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
                    
                    # Also display individual results in expandable sections
                    for idx, result in enumerate(processed_results, 1):
                        with st.expander(f"Result {idx}: {result['title'][:50]}...", expanded=False):
                            st.markdown(f"""
                                ### Details
                                **Price**: {result['price']}  
                                **Source**: [{result['title']}]({result['url']})
                                
                                ---
                                """)
                else:
                    st.warning("No results found for this VIN number.")
        else:
            st.error("Please enter a VIN number")

main()
    