from sentiment import Sentiment
from ner import NER
import os
import json

def lambda_handler(event, context):
  recognized_reviews = NER(event, False).recognize_words() # recognize the words
  final_json = Sentiment(recognized_reviews, 0.5,0.5, 0.2).calculate_final_json() # return the top words
  return final_json

if __name__ == "__main__":
  json_file_path = os.getcwd() + '/src1/entity/scrapped_restaurant_reviews/restaurant.json'
  with open(json_file_path, 'r') as f:
    contents = json.load(f)
  final = lambda_handler(contents, 1)
  print(final)
  # print(type(contents))

