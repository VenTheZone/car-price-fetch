# VIN Price Searcher

A Streamlit-based web application that searches for vehicle prices across multiple automotive websites using VIN numbers.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/vin-price-searcher.git
cd vin-price-searcher
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Configure your Brave Search API key:
- Get your API key from the Brave Search Developer Portal
- Replace 'YOUR_BRAVE_API_KEY' in search_engines.py with your actual API key

## Usage

1. Run the Streamlit application:
```bash
streamlit run main.py
```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

3. Enter a VIN number and click "Search" to find prices across multiple automotive websites

## Features

- Multi-engine search using Brave Search and DuckDuckGo
- Concurrent processing for faster results
- Price extraction from web pages
- Progress indicators
- Duplicate result removal
- Clean user interface

## File Structure

- main.py: Main application file with Streamlit interface
- search_engines.py: Search engine integration
- price_extractor.py: Web scraping and price extraction
- requirements.txt: Project dependencies
- README.md: Project documentation
    