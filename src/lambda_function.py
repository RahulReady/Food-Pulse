import sys, os
'''
@Notes
1) To run this, just replace url with the restaurant you want.
2) Importing correctly??
3) Which link are we supposed to give the file again?

@TODO
[] Remove stopwords/ blanks that the model recognizes
'''

# Class imports
from review_scraper import GoogleReviewScraper
from Sentiment import Sentiment
from NER import NER

def lambda_handler(event, context):
  url = event["params"]["querystring"]["url"]

  local = False
  reviews = GoogleReviewScraper(local).get_reviews(url)

  return{
    'url': url,
    'reviews': reviews
  }

# Testing locally (need to add to the lambda_handler for prod test)
local = True
url = 'https://www.google.com/search?sa=X&sxsrf=ALeKk02WRkzy4UWSUj5L--CM2J0sLlQ0Eg:1608238223236&q=local%20restaurants&ved=2ahUKEwi48Img8tXtAhULCc0KHT0aBvQQvS4wAXoECAIQTQ&biw=1440&bih=821&dpr=2&tbs=lf:1,lf_ui:9&tbm=lcl&rflfq=1&num=10&rldimm=11554796041735669729&lqi=ChFsb2NhbCByZXN0YXVyYW50c0jPt9y85YCAgAhaJgoLcmVzdGF1cmFudHMQARgAGAEiEWxvY2FsIHJlc3RhdXJhbnRz&phdesc=9-phEQmr5jc&rlst=f#lrd=0x8824aef206d4730f:0xa05ae1c7afbe87e1,1,,,&rlfi=hd:;si:11554796041735669729,l,ChFsb2NhbCByZXN0YXVyYW50c0jPt9y85YCAgAhaJgoLcmVzdGF1cmFudHMQARgAGAEiEWxvY2FsIHJlc3RhdXJhbnRz,y,9-phEQmr5jc;mv:[[42.498045600000005,-83.4226791],[42.4273962,-83.48853820000001]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3american_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3japanese_1restaurant!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!1m4!1u22!2m2!21m1!1e1!2m1!1e2!2m1!1e5!2m1!1e1!2m1!1e3!3sIAEqAlVT,lf:1,lf_ui:9'
scraper = GoogleReviewScraper(local).get_reviews(url) # stores the reviews
NER(True).main() # recognize the words
Sentiment(0.3,0.7, 0.2).main() # return the top words