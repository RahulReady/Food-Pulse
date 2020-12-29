import os
import time
import json
import math
from selenium import webdriver

SCROLL_REFRESH_TIME = 1
REVIEWS_PER_SCROLL = 10

class GoogleReviewScraper:
    def __init__(self, local):
        self._driver = self._get_driver(local)
        self._dialog_box = None
        self._nbr_of_scrolls = 0
        self._general_info = {}

    # Init the driver with chromedriver and related options
    def _get_driver(self, local):
        chrome_options = webdriver.ChromeOptions()

        if local:
            # chrome_options.add_argument("--headless")
            loc = os.getcwd() + '/src/chromedriver'
            print(loc)
            driver = webdriver.Chrome(loc, options=chrome_options)

        else:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--user-data-dir=/tmp/user-data')
            chrome_options.add_argument('--hide-scrollbars')
            chrome_options.add_argument('--enable-logging')
            chrome_options.add_argument('--log-level=0')
            chrome_options.add_argument('--v=99')
            chrome_options.add_argument('--single-process')
            chrome_options.add_argument('--data-path=/tmp/data-path')
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--homedir=/tmp')
            chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument(
                'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
            chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium" 
            driver = webdriver.Chrome(chrome_options=chrome_options)

        return driver

    # Utility function to scroll, using the thumbs up button as an anchor
    def _scroll(self):
        thumbs_up = self._dialog_box.find_elements_by_class_name("tdBFC")
        
        # Find the last found thumbs up and scroll until there
        self._driver.execute_script("arguments[0].scrollIntoView(true);", thumbs_up[-1])

    # Click all the more links to expand reviews
    def _expand_reviews(self):
        more_links = self._dialog_box.find_elements_by_class_name("review-more-link")
        for link in more_links:
            link.click()

    # Scrape general information about the restaurant and reviews
    def _get_general_info(self):
        restaurant_name = self._driver.find_element_by_class_name("P5Bobd")
        review_score_container = self._dialog_box.find_element_by_class_name("review-score-container")
        overall_rating = review_score_container.find_element_by_class_name("Aq14fc")
        nbr_of_reviews = review_score_container.find_element_by_class_name("z5jxId")
        self._general_info = {
            "restaurant_name": restaurant_name.text,
            "overall_rating": overall_rating.text,
            "nbr_of_reviews": nbr_of_reviews.text.split()[0].replace(",", "")
        }
        self._nbr_of_scrolls = math.ceil( int(self._general_info['nbr_of_reviews']) / REVIEWS_PER_SCROLL )

    # Parse all the available reviews
    def _parse_reviews(self):
        parsed_reviews = []
        reviews_text = []
        stars = []
        review_boxes = self._dialog_box.find_elements_by_class_name("Jtu6Td")
        review_stars = self._dialog_box.find_elements_by_class_name("EBe2gf")

        print("nbr of reviews: " + str(len(review_boxes)))
        
        # Get the text of each individual review
        for review in review_boxes:
            reviews_text.append(review.text)


        for star in review_stars:
            label = star.get_attribute("aria-label")
            stars.append(label.split()[1])
        
        # Create json type structure
        for i in range(len(review_boxes)):
            review_data = {
                "rating": stars[i],
                "review": reviews_text[i]
            }
            parsed_reviews.append(review_data)

        return parsed_reviews

    # Main function to scrape all the info about the reviews
    def get_reviews(self, url):
        self._driver.implicitly_wait(100)

        print(url)

        # Open the specified URL
        self._driver.get(url)

        self._dialog_box = self._driver.find_element_by_class_name("review-dialog-body")

        self._get_general_info()

        for i in range(self._nbr_of_scrolls):
            print("scroll nbr: " + str(i))
            self._scroll()
            time.sleep(SCROLL_REFRESH_TIME)

        self._expand_reviews()

        reviews = self._parse_reviews()

        data = {
            "restaurant_name": self._general_info['restaurant_name'],
            "overall_rating": self._general_info['overall_rating'],
            "nbr_of_reviews": self._general_info['nbr_of_reviews'],
            "reviews": reviews,
        }

        self._driver.quit()
        # Saving json files for testing
        # _file = 'src/entity/scrapped_restaurant_reviews/restaurant.json'
        # with open(_file,'w') as json_file:
        #     json.dump(data, json_file)


        return json.dumps(data)


# print(type(reviews))
if __name__ == "__main__":
    url = 'https://www.google.com/search?sxsrf=ALeKk02pAGPH0ueOFtU6Q1Nj1shQfQTyBg:1608654859737&ei=AyDiX_vkOI25tAb1qrAo&q=restaurants%20springfield%20il&oq=restaurants+springfield+il&gs_lcp=CgZwc3ktYWIQAzIFCAAQyQMyAggAMgIIADICCAAyAggAMgIIADICCAAyBggAEBYQHjIGCAAQFhAeMgYIABAWEB46BAgAEEc6BAgjECc6BAgAEEM6DQguELEDEMcBEKMCEEM6CAguEMcBEK8BOggILhDHARCjAjoICAAQsQMQgwE6BwgAELEDEEM6BwgAEBQQhwI6CwguELEDEMcBEKMCOgcIIxDJAxAnOgUIABCSAzoFCAAQsQM6CggAELEDEBQQhwJQlxdYqDRg4TRoAHACeACAAWGIAZoQkgECMjWYAQCgAQGqAQdnd3Mtd2l6yAEIwAEB&sclient=psy-ab&ved=2ahUKEwio-uurguLtAhVaZc0KHaLdB-kQvS4wAHoECAIQQA&uact=5&tbs=lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3seafood_1restaurant!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!1m4!1u22!2m2!21m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3american_1restaurant!2m1!1e2!2m1!1e5!2m1!1e3!2m4!1e1!5m2!1m1!2u8!3sIAEqAlVT,lf:1,lf_ui:9&tbm=lcl&rflfq=1&num=10&rldimm=7945474418576427725&lqi=ChpyZXN0YXVyYW50cyBzcHJpbmdmaWVsZCBpbEiuhLz95YCAgAhaMQoLcmVzdGF1cmFudHMQABgAGAEYAiIacmVzdGF1cmFudHMgc3ByaW5nZmllbGQgaWw&phdesc=JExN5RlCb2U&rlst=f&rlfi=hd:;si:#lrd=0x887547c2e4df0dab:0x14782efc1922d5fb,1,,,&rlfi=hd:;si:1474980538252187131,l,ChpyZXN0YXVyYW50cyBzcHJpbmdmaWVsZCBpbFopCgtyZXN0YXVyYW50cyIacmVzdGF1cmFudHMgc3ByaW5nZmllbGQgaWw,y,1gGSZQkOuHM;mv:[[39.8394239,-89.60043139999999],[39.6892713,-89.7398781]]'
    
    # Are we running locally or on AWS lambda?
    local = True
    reviews = GoogleReviewScraper(local).get_reviews(url)
    