import streamlit as st
from search_engines import search_perplexity
from price_extractor import process_results
import concurrent.futures
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import BytesIO
import datetime

def main():
    st.title("Multi-Engine VIN Price Searcher")
    st.write("Enter a VIN number to search across multiple automotive websites")
    
    vin_input = st.text_input("VIN Number:", "")
    
    if st.button("Search"):
        if vin_input:
            with st.spinner("Searching..."):
                progress_text = st.empty()
                progress_bar = st.progress(0)
                
                progress_text.text("Searching Perplexity...")
                results = search_perplexity(vin_input)
                progress_bar.progress(100)
                
                progress_text.empty()
                
                # Combine and process results
                all_results = list(set(results))  # Remove duplicates
                
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
                        label=" Download Excel Report",
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
    