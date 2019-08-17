
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def start_chrome_locally():
    CHROMEDRIVER_PATH = '.chromedriver/bin/chromedriver'
    browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)

    return browser

def start_chrome_heroku():
    import os
    chrome_exec_shim = os.environ.get("GOOGLE_CHROME_BIN", "chromedriver")
    opts = webdriver.ChromeOptions()
    opts.binary_location = chrome_exec_shim
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--disable-gpu')
    CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
    browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=opts)

    return browser

def get_location(GMAIL, GMAIL_PASSWORD, PHONE_NAME, LOCALLY=True):
    '''
    Function that uses selenium to query Google's "Find my phone" website
    to obtain your phone's location.
    The phone name (PHONE_NAME variable) needs to be exact, as it is written
    on the "Find my phone" website: https://www.google.com/android/find?did=0
    This function opens the browser. 
    To avoid opening browsers, run the function with LOCALLY=False.
    This is intended at gui-less servers like heroku.
    IT PRESUMES A COUPLE OF ENVIRONMENT VARIABLES.
    '''

    # start chrome browser and control it with selenium
    if LOCALLY:
        browser = start_chrome_locally()
    else:
        browser = start_chrome_heroku()

    # Navigate to Google's page "Find your phone"
    url = 'https://www.google.com/android/find?did=0'
    browser.get(url)
    time.sleep(5)

    # Enter your credentials
    email = browser.find_element_by_xpath('//input[@type="email"]')
    email.send_keys(GMAIL)
    email.send_keys(Keys.ENTER)
    time.sleep(3)
    passw = browser.find_element_by_xpath('//input[@type="password"]')
    passw.send_keys(GMAIL_PASSWORD)
    passw.send_keys(Keys.ENTER)
    time.sleep(10)

    # click on your phone if you have multiple devices with same google account
    your_phone = browser.find_element_by_xpath('//img[@aria-label="{}"]'.format(PHONE_NAME))
    your_phone.click()
    time.sleep(2)

    # Get location or throw error and return 0,0 as lattitude and 
    # longitude location
    try:
        # click on the green arrow showing your location
        your_loc = browser.find_element_by_xpath('//div[@title=""]')
        your_loc.click()
        time.sleep(3)

        # switch to the newly opened window
        browser.switch_to.window(browser.window_handles[1])
        time.sleep(2)

        # get the location from the google maps url
        loc = browser.current_url.split('@')[1].split(',')
        lat, lng = loc[0], loc[1]

    except Exception as e:
        print('Exception when trying to use selenium to get location.')
        print('Exception: {}'.format(e))
        lat, lng = 0,0
    
    return lat,lng

if __name__ == "__main__":
    import argparse
    parser_of_args = argparse.ArgumentParser(description='Use selenium to query' +
                                                         'Google-s Find my phone' +
                                                         'website to get latitude' + 
                                                         'and longitude of your desired device')
    parser_of_args.add_argument('GMAIL', type=str,
                                help='Your gmail')
    parser_of_args.add_argument('GMAIL_PASSWORD',type=str,
                                help='Your gmail password')
    parser_of_args.add_argument('PHONE_NAME',type=str,
                                help='The device name you want the location for.' +
                                     'Exact device name as on the Find your phone website')
    parser_of_args.add_argument('--LOCALLY',type=str,
                                help='If you-re running the script locally or on heroku.'+
                                     'Check the function start_chrome_heroku for more info.')
    args = parser_of_args.parse_args()

    if args.LOCALLY:
        get_location(args.GMAIL, args.GMAIL_PASSWORD, args.PHONE_NAME, args.LOCALLY)
    else:
        args.LOCALLY = False
        get_location(args.GMAIL, args.GMAIL_PASSWORD, args.PHONE_NAME, args.LOCALLY)