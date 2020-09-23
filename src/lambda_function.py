import sys, os
# import importlib # Needed for testing changes to code

# Script Imports
from review_scraper import *
# from NLP_script import test10, test11

# Following code needed if the Processing Pipeline scripts are updated
# importlib.reload(src.NLP_script)
# importlib.reload(src.scraping_reviews)

def lambda_handler(event, context):
  # url = event["params"]["querystring"]["url"]

  url = 'https://www.google.com/search?tbm=lcl&ei=N89BX9vFA4W8tgWo0IZw&q=taco+bell+near+me&oq=taco+bell+near+me&gs_l=psy-ab.3..0i433k1j0i402k1l2j0l7.11900.13773.0.13894.17.17.0.0.0.0.185.1810.4j11.15.0....0...1c.1.64.psy-ab..2.15.1806...46i433i199i291k1j0i433i67k1j0i433i131k1j46i433i131k1j0i273k1j0i433i131i67k1j46i433i199i291i67k1j46i199i175i273k1j0i67k1j46i67k1j46i433i67k1j46i199i291k1j46i199i291i273k1j46i433i199i291i273k1j46i199i175k1j46i433i131i199i291k1j46i433i199i175k1j46i433k1.0.OYwv7nQlq2Q#lrd=0x880ef836eeffd645:0xa1cef5135672adf5,1,,,&rlfi=hd:;si:11659525948712332789,l,ChF0YWNvIGJlbGwgbmVhciBtZSIGiAEBkAEBSIGP5MnlgICACFoqCgl0YWNvIGJlbGwQABABGAAYARgCGAMiEXRhY28gYmVsbCBuZWFyIG1l;mv:[[41.89154740000001,-88.0502388],[41.697815299999995,-88.3868498]]'
  
  scraper = GoogleReviewScraper()
  reviews = scraper.get_reviews(url)

  return{
    'url': url,
    'reviews': reviews
  }
  