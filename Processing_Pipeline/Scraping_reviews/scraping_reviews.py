import os
from selenium import webdriver
import time
# TODO
# [X] Baseline script
# [] Do headless stuff after finishing using normal webdriver?
# [] Do X number of scrolls or scroll till end for reviews?
# [] Store reviews in a DF
# [] Send df to NLP script
# [] How to pass in url to this script from the chrome extension?

# Chromedriver setup
def setup():
    # Pointing to downloaded chromedriver
    driver_location = os.getcwd() + '/Processing_Pipeline/Scraping_reviews/chrome_driver/chromedriver'
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(driver_location)
    return driver

# Reading the current url
def read_data(driver, url):
    # Open the specified URL
    driver.get(url);

    # Do processing stuff here ***************** CODE MAGIC GOES HERE
    print('success')
    time.sleep(3)

    # Initial idea
    # Store the data in a dataframe and finally pass that dataframe into the NLP script


    # Quitting the driver
    driver.quit()

    # Return reviews df

if __name__ == "__main__":
    # Have to somehow pass in the page the user is looking at

    # Shoutout to Rohan
    url = 'https://www.google.com/search?tbm=lcl&ei=N89BX9vFA4W8tgWo0IZw&q=taco+bell+near+me&oq=taco+bell+near+me&gs_l=psy-ab.3..0i433k1j0i402k1l2j0l7.11900.13773.0.13894.17.17.0.0.0.0.185.1810.4j11.15.0....0...1c.1.64.psy-ab..2.15.1806...46i433i199i291k1j0i433i67k1j0i433i131k1j46i433i131k1j0i273k1j0i433i131i67k1j46i433i199i291i67k1j46i199i175i273k1j0i67k1j46i67k1j46i433i67k1j46i199i291k1j46i199i291i273k1j46i433i199i291i273k1j46i199i175k1j46i433i131i199i291k1j46i433i199i175k1j46i433k1.0.OYwv7nQlq2Q#lrd=0x880ef836eeffd645:0xa1cef5135672adf5,1,,,&rlfi=hd:;si:11659525948712332789,l,ChF0YWNvIGJlbGwgbmVhciBtZSIGiAEBkAEBSIGP5MnlgICACFoqCgl0YWNvIGJlbGwQABABGAAYARgCGAMiEXRhY28gYmVsbCBuZWFyIG1l;mv:[[41.89154740000001,-88.0502388],[41.697815299999995,-88.3868498]]'
    driver = setup()
    read_data(driver, url)
