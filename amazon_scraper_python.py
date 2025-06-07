import os
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration
AMAZON_URL = "https://www.amazon.com"

# STEP 1: Configure your Bright Data Browser API endpoint
# - Get endpoint from: https://brightdata.com/cp/zones
# - Create new Browser API: https://docs.brightdata.com/scraping-automation/scraping-browser/quickstart
# - HTTP format: https://brd-customer-[id]-zone-[zone]:[password]@brd.superproxy.io:9515
BROWSER_API = os.getenv("BRIGHT_DATA_BROWSER_API_ENDPOINT", 'YOUR_BRIGHT_DATA_BROWSER_API_ENDPOINT')

# STEP 2: Run `python amazon_product_scraping.py` command in terminal

# Search parameters
SEARCH_TERM = "laptop"  # Change this to search for different products

def scrape_amazon():
    """
    Main function to run the scraper
    This is the entry point of our script
    """
    print("🚀 Starting Amazon scraper...")
    print(f"🔍 Searching for: {SEARCH_TERM}")

    try:
        # Step 1: Connect to Bright Data's browser
        print("🌐 Connecting to browser...")
        sbr_connection = ChromiumRemoteConnection(BROWSER_API, 'goog', 'chrome')
        browser = Remote(sbr_connection, options=ChromeOptions())
        print("✅ Connected to browser")

        # Step 3: Go to Amazon
        print("🌐 Opening Amazon...")
        browser.get(AMAZON_URL)
        print("✅ Amazon loaded")

        # Step 4: Search for products
        print("🔍 Entering search term...")
        search_box = browser.find_element(By.ID, 'twotabsearchtextbox')
        search_box.send_keys(SEARCH_TERM)
        browser.find_element(By.ID, 'nav-search-submit-button').click()
        print("✅ Search submitted")

        # Step 5: Wait for results to load
        print("⏳ Waiting for results...")
        WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-component-type="s-search-result"]'))
        )
        print("✅ Results loaded")

        # Step 6: Extract product information
        print("📊 Extracting product data...")
        
        # Get all product elements
        product_elements = browser.find_elements(By.CSS_SELECTOR, '[data-component-type="s-search-result"]')
        
        products = []
        # Process only first 5 products
        for item in product_elements[:5]:
            # Get product title
            try:
                title_element = item.find_element(By.CSS_SELECTOR, 'h2')
                title = title_element.text
            except:
                title = 'N/A'

            # Get product price
            try:
                price_element = item.find_element(By.CSS_SELECTOR, '.a-price .a-offscreen')
                price = price_element.text
            except:
                price = 'N/A'

            # Get product rating
            try:
                rating_element = item.find_element(By.CSS_SELECTOR, '.a-icon-star-small')
                rating = rating_element.text
            except:
                rating = 'N/A'

            products.append({
                'title': title,
                'price': price,
                'rating': rating
            })

        # Step 7: Display results
        print(f"\n📊 AMAZON SEARCH RESULTS for \"{SEARCH_TERM}\"")
        print("=======================")
        
        # Format and display each product in a clean, readable way
        for index, product in enumerate(products):
            print(f"\n#{index + 1} {product['title']}")
            print(f"   💰 Price: {product['price']}")
            print(f"   ⭐ Rating: {product['rating']}")
            print("   " + "-" * 50)
        
        print(f"\n✅ Found {len(products)} products for \"{SEARCH_TERM}\"")

        # Step 8: Close browser
        print("👋 Closing browser...")
        browser.quit()
        print("✅ Browser closed")

    except Exception as error:
        print(f"❌ Error occurred: {error}")

# Run the scraper
if __name__ == "__main__":
    scrape_amazon()
