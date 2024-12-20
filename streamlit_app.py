import streamlit as st
from search_engines import search_brave, search_duckduckgo
from price_extractor import process_results
import concurrent.futures

def main():
    st.title("Multi-Engine VIN Price Searcher")
    st.write("Enter a VIN number to search across multiple automotive websites")
    
    vin_input = st.text_input("VIN Number:", "")
    
    if st.button("Search"):
        if vin_input:
            with st.spinner("Searching..."):
                # Create progress bars
                brave_progress = st.progress(0)
                ddg_progress = st.progress(0)
                
                # Search using both engines
                brave_results = search_brave(vin_input)
                brave_progress.progress(100)
                
                ddg_results = search_duckduckgo(vin_input)
                ddg_progress.progress(100)
                
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
                    
                    for idx, result in enumerate(processed_results, 1):
                        st.write(f"\n--- Result {idx} ---")
                        st.write(f"Title: {result['title']}")
                        st.write(f"Price: {result['price']}")
                        st.write(f"URL: {result['url']}")
                        st.markdown("---")
                else:
                    st.warning("No results found for this VIN number.")
        else:
            st.error("Please enter a VIN number")

if __name__ == "__main__":
    main()
 