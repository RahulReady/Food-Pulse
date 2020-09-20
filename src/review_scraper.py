import os
import time
import json
import math
from selenium import webdriver

SCROLL_REFRESH_TIME = 1
REVIEWS_PER_SCROLL = 10

class GoogleReviewScraper:
    def __init__(self):
        self.driver = self.__get_driver()
        self.dialog_box = None
        self.nbr_of_scrolls = 0
        self.general_info = {}

    # Init the driver with chromedriver and related options
    def __get_driver(self):
        driver_location = os.getcwd() + '/lib/chromedriver'
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        driver = webdriver.Chrome(driver_location, options=options)
        
        return driver

    # Utility function to scroll, using the thumbs up button as an anchor
    def __scroll(self):
        thumbs_up = self.dialog_box.find_elements_by_class_name("tdBFC")
        
        # Find the last found thumbs up and scroll until there
        self.driver.execute_script("arguments[0].scrollIntoView(true);", thumbs_up[-1])

    # Click all the more links to expand reviews
    def __expand_reviews(self):
        more_links = self.dialog_box.find_elements_by_class_name("review-more-link")
        for link in more_links:
            link.click()

    # Scrape general information about the restaurant and reviews
    def __get_general_info(self):
        restaurant_name = self.driver.find_element_by_class_name("P5Bobd")
        review_score_container = self.dialog_box.find_element_by_class_name("review-score-container")
        overall_rating = review_score_container.find_element_by_class_name("Aq14fc")
        nbr_of_reviews = review_score_container.find_element_by_class_name("z5jxId")
        self.general_info = {
            "restaurant_name": restaurant_name.text,
            "overall_rating": overall_rating.text,
            "nbr_of_reviews": nbr_of_reviews.text.split()[0]
        }
        self.nbr_of_scrolls = math.ceil( int(self.general_info['nbr_of_reviews']) / REVIEWS_PER_SCROLL )

    # Parse all the available reviews
    def __parse_reviews(self):
        parsed_reviews = []
        review_boxes = self.dialog_box.find_elements_by_class_name("Jtu6Td")
        # review_stars = dialog_box.find_elements_by_xpath("//label[contains(text(),'Rated')]")

        print("nbr of reviews: " + str(len(review_boxes)))
        
        # Get the text of each individual review
        for review in review_boxes:
            stars = "4"
            parsed_reviews.append({"stars":stars, "review":review.text})

        return parsed_reviews

    # Main function to scrape all the info about the reviews
    def get_reviews(self, url):
        self.driver.implicitly_wait(100)

        # Open the specified URL
        self.driver.get(url)

        self.dialog_box = self.driver.find_element_by_class_name("review-dialog-body")

        self.__get_general_info()

        for i in range(self.nbr_of_scrolls):
            self.__scroll()
            time.sleep(SCROLL_REFRESH_TIME)

        self.__expand_reviews()

        reviews = self.__parse_reviews()

        data = {
            "restaurant_name": self.general_info['restaurant_name'],
            "overall_rating": self.general_info['overall_rating'],
            "nbr_of_reviews": self.general_info['nbr_of_reviews'],
            "reviews": reviews,
        }

        driver.quit()

        return json.dumps(data)
    

if __name__ == "__main__":
    url = 'https://www.google.com/search?tbm=lcl&ei=N89BX9vFA4W8tgWo0IZw&q=taco+bell+near+me&oq=taco+bell+near+me&gs_l=psy-ab.3..0i433k1j0i402k1l2j0l7.11900.13773.0.13894.17.17.0.0.0.0.185.1810.4j11.15.0....0...1c.1.64.psy-ab..2.15.1806...46i433i199i291k1j0i433i67k1j0i433i131k1j46i433i131k1j0i273k1j0i433i131i67k1j46i433i199i291i67k1j46i199i175i273k1j0i67k1j46i67k1j46i433i67k1j46i199i291k1j46i199i291i273k1j46i433i199i291i273k1j46i199i175k1j46i433i131i199i291k1j46i433i199i175k1j46i433k1.0.OYwv7nQlq2Q#lrd=0x880ef836eeffd645:0xa1cef5135672adf5,1,,,&rlfi=hd:;si:11659525948712332789,l,ChF0YWNvIGJlbGwgbmVhciBtZSIGiAEBkAEBSIGP5MnlgICACFoqCgl0YWNvIGJlbGwQABABGAAYARgCGAMiEXRhY28gYmVsbCBuZWFyIG1l;mv:[[41.89154740000001,-88.0502388],[41.697815299999995,-88.3868498]]'
    
    scraper = GoogleReviewScraper()
    reviews = scraper.get_reviews(url)