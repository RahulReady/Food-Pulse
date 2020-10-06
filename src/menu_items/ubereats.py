## Adapted from another project: https://github.com/salik95/Ubereats-Scraper ##

import os, time, csv
from selenium import webdriver

FILENAME = 'ubereats.csv'
CITY_NAMES_TSV = 'ubereatsURL.tsv'

class UberEatsScraper:
    def __init__(self):
        self._driver = self._get_driver()
        self._city_urls = self._get_city_urls()
        self._food_names = []

    # Init the driver with chromedriver and related options
    def _get_driver(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")

        loc = os.getcwd() + '../chromedriver'
        driver = webdriver.Chrome(loc, options=chrome_options)
        
        return driver

    # Get all the city urls from the TSV file
    def _get_city_urls(self):
        urls = []
        with open(CITY_NAMES_TSV) as tsvfile:
            for item in tsvfile:
                urls.append(item.split('\t')[1].strip('\n').strip())
        
        return urls

    # Get all the restaurant urls from a certain city
    def _get_restaurant_urls(self):
        urls = []

        # Find container box
        try:
            box = self._driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[1]/main[1]/div[6]')
        except:
            return urls #len is 0 here

        # Scroll and grab all the restaurant URLs
        lenOfPage = self._driver.execute_script("var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        current_position = 1000
        while current_position < lenOfPage:
            self._driver.execute_script("window.scrollTo(0, " + str(current_position)+ ")")
            # Find all the restaurant urls on the page
            restaurant_urls = box.find_elements_by_tag_name('a')
            time.sleep(0.25)
            for url in restaurant_urls:
                try:
                    urls.append(url.get_attribute('href'))
                except:
                    pass
            current_position = current_position + 1000
        
        return set(urls)

    # Get all the food names from a certain restaurant
    def _get_food_names(self):
        # Click that button that shows up asking to enter an address
        try:
            button = self._driver.find_element_by_css_selector("[aria-label=Close]").click()
        except:
            pass

        list_items = self._driver.find_elements_by_tag_name('li')
        for list_item in list_items:
            names = list_item.find_elements_by_tag_name('h4')
            for name in names:
                self._food_names.append(name.text)
        
        # Remove all duplicates
        self._food_names = list( dict.fromkeys(self._food_names) )

    def _write_to_csv(self):
        with open(FILENAME, 'w') as fp:
            fieldnames = ['food_name']
            writer = csv.DictWriter(fp, fieldnames=fieldnames)

            writer.writeheader()
            for i in range(len(self._food_names)):
                writer.writerow({'food_name': self._food_names[i]})

    def scrape_food_names(self):
        # Open city URLs one by one
        for url in self._city_urls:
            try:
                self._driver.get(url)
            except:
                continue

            restaurant_urls = self._get_restaurant_urls()
            if len(restaurant_urls) == 0:
                continue

            # Open all the restaurant URLs one by one
            for url in restaurant_urls:
                try:
                    self._driver.get(url)
                except:
                    continue

                self._get_food_names()
                self._write_to_csv()
            

if __name__ == "__main__":
    scraper = UberEatsScraper()
    scraper.scrape_food_names()