import sys, os
# import importlib # Needed for testing changes to code

# Script Imports
from review_scraper import *
# from NLP_script import test10, test11

# Following code needed if the Processing Pipeline scripts are updated
# importlib.reload(src.NLP_script)
# importlib.reload(src.scraping_reviews)

def lambda_handler(event, context):
  url = event["params"]["querystring"]["url"]

  local = False
  scraper = GoogleReviewScraper(local)
  reviews = scraper.get_reviews(url)

  return{
    'url': url,
    'reviews': reviews
  }
  