import os
from datetime import datetime, timedelta
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration
BOOKING_URL = "https://www.booking.com/"

# STEP 1: Configure your Bright Data Browser API endpoint
# - Get endpoint from: https://brightdata.com/cp/zones
# - Create new Browser API: https://docs.brightdata.com/scraping-automation/scraping-browser/quickstart
# - HTTP format: https://brd-customer-[id]-zone-[zone]:[password]@brd.superproxy.io:9515
BROWSER_API = os.getenv("BRIGHT_DATA_BROWSER_API_ENDPOINT", "https://brd-customer-hl_7abed23d-zone-scraping_browser2:6ttcf7cx7ix4@brd.superproxy.io:9515")

# STEP 2: Run `python booking_hotel_scraping.py` command in terminal

# Search parameters
SEARCH_LOCATION = "New York"
CHECK_IN_DAYS_FROM_NOW = 1   # Check-in tomorrow
CHECK_OUT_DAYS_FROM_NOW = 2  # Check-out day after tomorrow

def add_days(date, days):
    """Helper function to add days to a date"""
    return date + timedelta(days=days)

def format_date(date):
    """Helper function to format date for Booking.com"""
    return date.strftime('%Y-%m-%d')

# Calculate check-in and check-out dates
today = datetime.now()
check_in_date = format_date(add_days(today, CHECK_IN_DAYS_FROM_NOW))
check_out_date = format_date(add_days(today, CHECK_OUT_DAYS_FROM_NOW))

def search_hotels():
    """Main function to run the hotel search"""
    print("🔍 Starting hotel search process...")
    print(f"📍 Searching for hotels in: {SEARCH_LOCATION}")
    print(f"📅 Check-in date: {check_in_date}")
    print(f"📅 Check-out date: {check_out_date}")
    
    try:
        # Connect to browser
        print("🌐 Connecting to browser...")
        sbr_connection = ChromiumRemoteConnection(BROWSER_API, 'goog', 'chrome')
        browser = Remote(sbr_connection, options=ChromeOptions())
        print("✅ Successfully connected to browser")
        
        # Open Booking.com
        print("🌐 Opening Booking.com...")
        browser.get(BOOKING_URL)
        print("✅ Successfully loaded Booking.com")
        
        # Handle popup if it appears
        handle_popup(browser)
        
        # Fill search form and submit
        print("📝 Filling search form...")
        fill_search_form(browser)
        print("✅ Search form submitted successfully")
        
        # Get and display results
        print("🔍 Searching for available hotels...")
        results = get_hotel_results(browser)
        
        # Display results in a table format
        print("\n📊 Search Results:")
        print("==================")
        
        # Display results
        for index, hotel in enumerate(results, 1):
            print(f"\n#{index}")
            print(f"Hotel Name: {hotel['name']}")
            print(f"Price: {hotel['price']}")
            print(f"Rating: {hotel['rating']}")
            print("-" * 50)
        
        print(f"\n✅ Found {len(results)} hotels")
        
        # Close browser
        print("👋 Closing browser...")
        browser.quit()
        print("✅ Browser closed successfully")
        
    except Exception as error:
        print(f"❌ Error occurred: {error}")

def handle_popup(page):
    """Handle the sign-in popup if it appears"""
    try:
        print("⚠️ Checking for popup...")
        close_button = WebDriverWait(page, 25).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Dismiss sign-in info."]'))
        )
        close_button.click()
        print("✅ Popup closed successfully")
    except Exception as e:
        print("ℹ️ No popup appeared - continuing with search")

def fill_search_form(page):
    """Fill and submit the search form"""
    # Fill location
    print("📍 Entering search location...")
    WebDriverWait(page, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="destination-container"] input'))
    )
    location_input = page.find_element(By.CSS_SELECTOR, '[data-testid="destination-container"] input')
    location_input.clear()
    location_input.send_keys(SEARCH_LOCATION)
    print("✅ Location entered successfully")
    
    # Select dates
    print("📅 Selecting dates...")
    page.find_element(By.CSS_SELECTOR, '[data-testid="searchbox-dates-container"]').click()
    WebDriverWait(page, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="searchbox-datepicker-calendar"]'))
    )
    page.find_element(By.CSS_SELECTOR, f'[data-date="{check_in_date}"]').click()
    page.find_element(By.CSS_SELECTOR, f'[data-date="{check_out_date}"]').click()
    print("✅ Dates selected successfully")
    
    # Submit search
    print("🔍 Submitting search...")
    page.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    print("✅ Search submitted successfully")

def get_hotel_results(page):
    """Extract hotel information from search results"""
    print("🏨 Extracting hotel information...")
    
    # Wait for results to load
    WebDriverWait(page, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="property-card"]'))
    )
    
    # Get all hotel card elements
    hotel_cards = page.find_elements(By.CSS_SELECTOR, '[data-testid="property-card"]')
    
    results = []
    for card in hotel_cards:
        # Extract hotel name
        try:
            name_element = card.find_element(By.CSS_SELECTOR, '[data-testid="title"]')
            name = name_element.text
        except:
            name = 'N/A'
        
        # Extract price
        try:
            price_element = card.find_element(By.CSS_SELECTOR, '[data-testid="price-and-discounted-price"]')
            price = price_element.text
        except:
            price = 'N/A'
        
        # Extract rating
        try:
            rating_element = card.find_element(By.CSS_SELECTOR, '[data-testid="review-score"]')
            rating = rating_element.text
        except:
            rating = 'N/A'
        
        results.append({
            'name': name,
            'price': price,
            'rating': rating
        })
    
    return results

# Start the search
if __name__ == "__main__":
    search_hotels()