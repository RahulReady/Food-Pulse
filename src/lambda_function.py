import sys, os
'''
@Notes
1) To run this, just replace url with the restaurant you want.
2) Importing correctly??
3) Which link are we supposed to give the file again?

@TODO
[] Remove stopwords/ blanks that the model recognizes
[] Make sure only the used packages are uploaded (refresh the requirements)
[] Why are the reviews limited to 60? 
'''

# Class imports
from review_scraper import GoogleReviewScraper
from Sentiment import Sentiment
from NER import NER

def lambda_handler(event, context):
  # url = event["params"]["querystring"]["url"]

  local = False
  url = 'https://www.google.com/search?sxsrf=ALeKk00sF7Cd7DbPJktAmB3JuY1I8fvWEA:1602444823747&q=local%20restaurants&npsic=0&rflfq=1&rldoc=1&rlha=0&rllag=41777374,-88209195,433&tbm=lcl&sa=X&ved=2ahUKEwjh5_aTpK3sAhXDVs0KHfBWA5IQjGp6BAgNEGI&biw=1440&bih=821&rlfi=hd:;si:&tbs=lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3american_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3seafood_1restaurant!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!1m4!1u22!2m2!21m1!1e1!2m1!1e5!2m1!1e1!2m1!1e3!2m4!1e2!5m2!2m1!2e9!3sIAEqAlVT,lf:1,lf_ui:9&rlst=f#lrd=0x880ef934af97c5e9:0x8816413c99534c2e,1,,,&rlfi=hd:;si:9806096967172049966,l,ChFsb2NhbCByZXN0YXVyYW50c1ogCgtyZXN0YXVyYW50cyIRbG9jYWwgcmVzdGF1cmFudHM,y,aEKRqBPTJWY;mv:[[41.7972548,-88.14491],[41.7510391,-88.2556199]]'
  GoogleReviewScraper(local).get_reviews(url)
  NER(False).main() # recognize the words
  reviews = Sentiment(0.3,0.7, 0.2).main() # return the top words
  print(reviews)
  # return{
  #   'url': url,
  #   'reviews': reviews
  # }
