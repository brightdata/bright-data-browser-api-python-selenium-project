# Bright Data Hotel Search Scraper with Selenium

This project demonstrates how to use Bright Data's Browser API with Selenium to search for hotels on Booking.com. It provides a practical example of web scraping with automated browser control using Selenium.

<a href="https://codesandbox.io/p/devbox/github/brightdata/bright-data-browser-api-python-selenium-project?file=%2Fbooking_hotel_scraping.py" target="_blank" rel="noopener">Open in CodeSandbox</a>, sign in with GitHub account, then fork the repository to begin making changes.

### Getting Started

1. Replace `YOUR_BRIGHT_DATA_BROWSER_API_ENDPOINT` with your actual Bright Data Browser API HTTP endpoint in `booking_hotel_scraping.py`
2. Run `python booking_hotel_scraping.py` to start scraping

## 💻 Usage

1. Modify search parameters in `booking_hotel_scraping.py`:
   ```python
   SEARCH_LOCATION = "New York"  # Change to your desired location
   CHECK_IN_DAYS_FROM_NOW = 1    # Adjust check-in date
   CHECK_OUT_DAYS_FROM_NOW = 2   # Adjust check-out date
   ```

2. Run the script:
   ```bash
   python booking_hotel_scraping.py
   ```

## 📊 Example Output

```
📊 Search Results:
==================

#1
Hotel Name: Hotel Name 1
Price: $100
Rating: 8.5
--------------------------------------------------

#2
Hotel Name: Hotel Name 2
Price: $150
Rating: 9.0
--------------------------------------------------

#3
Hotel Name: Hotel Name 3
Price: $200
Rating: 8.8
--------------------------------------------------

✅ Found 3 hotels
```