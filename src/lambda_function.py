import sys, os
'''
@Notes
1) To run this, just replace url with the restaurant you want.

@TODO
[] Make sure only the used packages are uploaded (refresh the requirements)
'''
# Class imports
from review_scraper import GoogleReviewScraper
from sentiment import Sentiment
from ner import NER
import time






def lambda_handler(event, context):
  # url = event["params"]["querystring"]["url"]
  start = time.time()

  local = False
  url = 'https://www.google.com/search?sxsrf=ALeKk00TFMQUFMP0MHhLO5XNq815N0Fs7g:1608672043405&q=saravana%20bhavan%20nyc&sa=X&ved=2ahUKEwjw09OtwuLtAhUQB50JHcORDusQvS4wAXoECAEQJQ&biw=1440&bih=821&dpr=2&tbs=lf:1,lf_ui:4&tbm=lcl&rflfq=1&num=10&rldimm=3279191070432345557&lqi=ChNzYXJhdmFuYSBiaGF2YW4gbnljIgOIAQFIvMy5huaAgIAIWi4KD3NhcmF2YW5hIGJoYXZhbhAAEAEYARgCIhNzYXJhdmFuYSBiaGF2YW4gbnljmgEjQ2haRFNVaE5NRzluUzBWSlEwRm5TVU13WDFrM2VVTjNFQUU&rlst=f#lrd=0x89c25888a5e913a9:0x2d8206e797c0bdd5,1,,,&rlfi=hd:;si:3279191070432345557,l,ChNzYXJhdmFuYSBiaGF2YW4gbnljIgOIAQFIvMy5huaAgIAIWi4KD3NhcmF2YW5hIGJoYXZhbhAAEAEYARgCIhNzYXJhdmFuYSBiaGF2YW4gbnljmgEjQ2haRFNVaE5NRzluUzBWSlEwRm5TVU13WDFrM2VVTjNFQUU;mv:[[40.7861119,-73.9774333],[40.7388926,-73.983409]]'
  GoogleReviewScraper(local).get_reviews(url)

  NER(False).recognize_words() # recognize the words
  final_json = Sentiment(0.5,0.5, 0.2).calculate_final_json() # return the top words
  end = time.time()
  print('time taken', end - start)
  print(final_json)
  # return{
  #   'url': url,
  #   'reviews': reviews
  # }

print('test')

# local = True
# url = 'https://www.google.com/search?sxsrf=ALeKk00TFMQUFMP0MHhLO5XNq815N0Fs7g:1608672043405&q=saravana%20bhavan%20nyc&sa=X&ved=2ahUKEwjw09OtwuLtAhUQB50JHcORDusQvS4wAXoECAEQJQ&biw=1440&bih=821&dpr=2&tbs=lf:1,lf_ui:4&tbm=lcl&rflfq=1&num=10&rldimm=3279191070432345557&lqi=ChNzYXJhdmFuYSBiaGF2YW4gbnljIgOIAQFIvMy5huaAgIAIWi4KD3NhcmF2YW5hIGJoYXZhbhAAEAEYARgCIhNzYXJhdmFuYSBiaGF2YW4gbnljmgEjQ2haRFNVaE5NRzluUzBWSlEwRm5TVU13WDFrM2VVTjNFQUU&rlst=f#lrd=0x89c25888a5e913a9:0x2d8206e797c0bdd5,1,,,&rlfi=hd:;si:3279191070432345557,l,ChNzYXJhdmFuYSBiaGF2YW4gbnljIgOIAQFIvMy5huaAgIAIWi4KD3NhcmF2YW5hIGJoYXZhbhAAEAEYARgCIhNzYXJhdmFuYSBiaGF2YW4gbnljmgEjQ2haRFNVaE5NRzluUzBWSlEwRm5TVU13WDFrM2VVTjNFQUU;mv:[[40.7861119,-73.9774333],[40.7388926,-73.983409]]'
# GoogleReviewScraper(local).get_reviews(url)
# NER(False).recognize_words() # recognize the words
# final_json = Sentiment(0.5,0.5, 0.2).calculate_final_json() # return the top words
# print(final_json)