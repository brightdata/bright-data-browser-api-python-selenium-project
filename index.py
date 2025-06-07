"""
Example of using Bright Data Browser API with Selenium WebDriver in Python
This simple script demonstrates how to make a request to a website through Bright Data Browser API
"""

import os
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

"""
STEP 1: Configure your Bright Data Browser API endpoint
 - Navigate to your Browser API zone from https://brightdata.com/cp/zones
 - Create your Browser API if you haven't already:
   https://docs.brightdata.com/scraping-automation/scraping-browser/quickstart
 - Copy your Selenium endpoint from the Browser API overview page:
   Example: https://brd-customer-hl_1user23d-zone-scraping_browser1:password12abcd@brd.superproxy.io:9515
 - Create a .env file in your project directory and add:
   BRIGHT_DATA_BROWSER_API_ENDPOINT=your_actual_endpoint_here
 - Or replace the fallback value below with your actual Browser API endpoint for Selenium
"""
BROWSER_API_ENDPOINT = os.getenv('BRIGHT_DATA_BROWSER_API_ENDPOINT', 'YOUR_BRIGHT_DATA_BROWSER_API_ENDPOINT')

# STEP 2: Set your target URL
PAGE_URL = "https://example.com"

# STEP 3: Install required packages and run the script
# pip install selenium python-dotenv
# python web_scraper.py

def main():
    """Main scraping function with proper error handling"""
    print("🚀 Starting the scraping process...")
    driver = None
    
    try:
        print("🌐 Setting up Selenium with Bright Data Browser API...")
        
        # Check if endpoint is configured
        if BROWSER_API_ENDPOINT == 'YOUR_BRIGHT_DATA_BROWSER_API_ENDPOINT':
            print("❌ Error: Please configure your Bright Data Browser API endpoint!")
            print("   Create a .env file with: BRIGHT_DATA_BROWSER_API_ENDPOINT=your_endpoint")
            print("   Or update the BROWSER_API_ENDPOINT variable in this script.")
            return
        
        # Initialize the WebDriver using Bright Data's Browser API
        sbr_connection = ChromiumRemoteConnection(BROWSER_API_ENDPOINT, 'goog', 'chrome')
        driver = Remote(sbr_connection, options=ChromeOptions())
        
        print("✅ Successfully connected to the browser!")
        
        # Navigate to the target URL
        print("🌍 Navigating to the test URL...")
        driver.get(PAGE_URL)
        
        # Take a screenshot
        print("📸 Taking a screenshot of the page...")
        driver.get_screenshot_as_file('./page.png')
        print("✅ Screenshot saved as 'page.png'!")
        
        # Get page content
        print("🔍 Scraping page content...")
        html = driver.page_source
        print("📝 Page content retrieved:")
        print(html)
        
        print("✅ Scraping completed successfully!")
        
    except Exception as error:
        print("❌ An error occurred during scraping:")
        print(f"   Error: {str(error)}")
        
        # Common troubleshooting tips
        if "not a package" in str(error):
            print("💡 Tip: Make sure your file is not named 'selenium.py'")
        elif "No module named" in str(error):
            print("💡 Tip: Install required packages with: pip install selenium python-dotenv")
        elif "Invalid argument" in str(error) or "connection" in str(error).lower():
            print("💡 Tip: Check your Bright Data endpoint URL and credentials")
            
    finally:
        if driver:
            driver.quit()
            print("👋 Browser closed.")

if __name__ == '__main__':
    main()