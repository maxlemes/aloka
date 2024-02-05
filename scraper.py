from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException
import sys
import csv

# read the ticker from the CLI argument
# ticker_symbol = 'LEVE3.SA'

# # build the URL of the target page
# url = f'https://finance.yahoo.com/quote/{ticker_symbol}'

def scrape_stock(driver, ticker_symbol):

    # build the URL of the target page
    url = f'https://finance.yahoo.com/quote/{ticker_symbol}'

    # visit the target page
    driver.get(url)

    try:
        # wait up to 3 seconds for the consent modal to show up
        consent_overlay = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.consent-overlay')))

        # click the 'Accept all' button
        accept_all_button = consent_overlay.find_element(By.CSS_SELECTOR, '.accept-all')
        accept_all_button.click()
    except TimeoutException:
        print('Cookie consent overlay missing')

    # initialize the stock dictionary with the
    # ticker symbol
    stock = { 'ticker': ticker_symbol }

    # Opens a new tab and switches to new tab
    # driver.switch_to.new_window('tab')

    # # Opens a new window and switches to new window
    # driver.switch_to.new_window('window')

    #Close the tab or window
    # driver.close()

    #Switch back to the old tab or window
    # driver.switch_to.window(original_window)

    # try:
    #     # wait up to 3 seconds for the consent modal to show up
    #     consent_overlay = WebDriverWait(driver, 3).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, '.consent-overlay')))

    #     # click the "Accept all" button
    #     accept_all_button = consent_overlay.find_element(By.CSS_SELECTOR, '.accept-all')
    #     accept_all_button.click()
    # except TimeoutException:
    #     print('Cookie consent overlay missing')


    regular_market_price = driver.find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="regularMarketPrice"]').text
    week_range = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="FIFTY_TWO_WK_RANGE-value"]').text
    volume = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="TD_VOLUME-value"]').text
    avg_volume = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="AVERAGE_VOLUME_3MONTH-value"]').text
    market_cap = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="MARKET_CAP-value"]').text
    beta = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="BETA_5Y-value"]').text
    pe_ratio = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="PE_RATIO-value"]').text
    eps = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="EPS_RATIO-value"]').text
    earnings_date = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="EARNINGS_DATE-value"]').text
    dividend_yield = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="DIVIDEND_AND_YIELD-value"]').text
    ex_dividend_date = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="EX_DIVIDEND_DATE-value"]').text
    year_target_est = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="ONE_YEAR_TARGET_PRICE-value"]').text

    # regular_market_change = driver\
    #     .find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="regularMarketChange"]')\
    #     .text
    # regular_market_change_percent = driver\
    #     .find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="regularMarketChangePercent"]')\
    #     .text\
    #     .replace('(', '').replace(')', '')

    # post_market_price = driver\
    #     .find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="postMarketPrice"]')\
    #     .text
    # post_market_change = driver\
    #     .find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="postMarketChange"]')\
    #     .text
    # post_market_change_percent = driver\
    #     .find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="postMarketChangePercent"]')\
    #     .text\
    #     .replace('(', '').replace(')', '')

    # initialize the dictionary
    # stock = {}

    # stock price scraping logic omitted for brevity...

    # add the scraped data to the dictionary
    stock['regular_market_price'] = regular_market_price
    stock['week_range'] = week_range
    stock['volume'] = volume
    stock['avg_volume'] = avg_volume
    stock['market_cap'] = market_cap
    stock['beta'] = beta
    stock['pe_ratio'] = pe_ratio
    stock['eps'] = eps
    stock['earnings_date'] = earnings_date
    stock['dividend_yield'] = dividend_yield
    stock['ex_dividend_date'] = ex_dividend_date
    stock['year_target_est'] = year_target_est
    # stock['regular_market_change'] = regular_market_change
    # stock['regular_market_change_percent'] = regular_market_change_percent
    # stock['post_market_price'] = post_market_price
    # stock['post_market_change'] = post_market_change
    # stock['post_market_change_percent'] = post_market_change_percent
    return stock

options = Options()
options.headless = True
options.add_argument("-headless")

driver = webdriver.Firefox(
    options=options
)

# Store the ID of the original window
original_window = driver.current_window_handle

# set up the window size of the controlled browser
driver.set_window_size(1150, 1080)

# the array containing all scraped data
stocks = []

# if there are no CLI parameters
# if len(sys.argv) <= 1:
#     print('Ticker symbol CLI argument missing!')
#     sys.exit(2)

tickers = ['LEVE3.SA', 'TUPY3.SA', 'SUZB3.SA']

# scraping all market securities
for ticker_symbol in tickers:
# for ticker_symbol in sys.argv[1:]:
    stocks.append(scrape_stock(driver, ticker_symbol))



# close the browser and free up the resources
driver.quit()


# extract the name of the dictionary fields
# to use it as the header of the output CSV file
csv_header = stocks[0].keys()

# export the scraped data to CSV
with open('stocks.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, csv_header)
    dict_writer.writeheader()
    dict_writer.writerows(stocks)
