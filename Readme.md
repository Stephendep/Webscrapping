
---

# Web SCRAPING PROJECT DOCUMENTATION

## Overview
This project scrapes product information from [First Planit](https://www.firstplanit.com/site/productlist). The script extracts details such as product URL, name, category, and document links. The data is saved in JSON format.

## Prerequisites
1. **Python**: Ensure Python (preferably Python 3.8 or newer) is installed.
2. **Chrome WebDriver**: This project uses Selenium, which requires a ChromeDriver compatible with your Chrome browser version. Download the appropriate version from [ChromeDriver - WebDriver for Chrome](https://sites.google.com/chromium.org/driver/).

## Installation

### Step 1: Set Up Virtual Environment
Create and activate a virtual environment to isolate dependencies.

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### Step 2: Install Required Packages
Use the provided `requirements.txt` to install dependencies.

```bash
pip install -r requirements.txt
```

The key libraries used are:
- `Selenium` for browser automation.
- `BeautifulSoup` for HTML parsing (if required).
- Additional libraries for managing HTTP requests and handling data.

## Script Overview
The main scraping logic is implemented in `scrap_data.py`. Here is a summary of the key components:

### `ProductScraper` Class
- **`__init__`**: Initializes the ChromeDriver and sets up the URL and page structure.
- **`_init_driver`**: Configures Chrome options for efficient scraping.
- **`wait_for_element`**: Waits for the required elements to load on each page.
- **`scrape_page`**: Scrapes product details including the name, category, URL, and document link.
- **`go_to_next_page`**: Automates pagination by navigating to the next page.
- **`save_to_json`**: Saves the scraped data in a JSON file (`product_data.json`).
- **`run`**: The main function that orchestrates scraping across multiple pages.

### Usage
To run the script:

```bash
python scrap_data.py
```

Ensure `chromedriver.exe` is in the same directory or provide its path when initializing the `ProductScraper`, use the latest chrome version.

## Example Output
The script saves data in `product_data.json` in the following format:

```json
[
    {
        "name": "Product Name",
        "category": "Category Name",
        "product_url": "https://www.example.com/product-link",
        "document": "https://www.example.com/document-link"
    },
    ...
]
```

## Notes
- **ChromeDriver Version**: Ensure ChromeDriver matches your Chrome browser version.
- **Error Handling**: The script includes basic error handling to skip over products that fail to load or extract data.
- Pop up login timed out the script from webscrapping all datas. which i will still work on
  
---
