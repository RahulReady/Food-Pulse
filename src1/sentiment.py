from ner import NER
from helper_functions import get_restaurant_review_path
import json
import math
from textblob import TextBlob
from nltk.tokenize import sent_tokenize, word_tokenize
# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

import nltk
# nltk.download('punkt') # local
nltk.data.path.append("/tmp")
nltk.download("punkt", download_dir = "/tmp")

class Sentiment:
    def __init__(self, reviews, sentence_weight, review_weight, threshold):
        # self.path = get_restaurant_review_path()
        self.reviews = reviews
        self.sentence_weight = sentence_weight
        self.review_weight = review_weight
        self.threshold = threshold

    def calculate_final_json(self):
        '''
        Input: None
        Output: Returns the final json of food items and their corresponding sentiment and nbr of occurrances
        '''
        # Read in reviews
        contents = self.reviews
        # with open(self.path, 'r') as f:
        #     contents = json.load(f)
        final_list = {"restaurant_name": contents['restaurant_name'], "food_ratings": None}
        running_total = {}
        for single_review in contents['reviews']:
            review_rating = single_review['rating']

            # If no foods, skip!
            if len(single_review['identified_foods']) == 0:
                continue
            else:
                # Tokenize sentences (God bless nltk)
                split_sentences = sent_tokenize(single_review['review'])

                for sent in split_sentences:
                    # Checks if the identified foods occurs in the current sentence.
                    for food_item in set(single_review['identified_foods']):
                        if food_item in sent:
                            # Sentiment calculations
                            if food_item in running_total:
                                # Update sentiment, count
                                running_total[food_item][0] = (running_total[food_item][0] + float(self.get_sentiment(sent))) / (running_total[food_item][1] + 1)
                                running_total[food_item][1] = running_total[food_item][1] + 1
                                running_total[food_item][2].append([sent,single_review["rating"]] )
                            else:
                                # Initialize sentiment, count 
                                combined_review_rating = float(self.get_sentiment(sent))
                                running_total[food_item] = [combined_review_rating, 1, [["",""]]]
                                running_total[food_item][2][0] = [sent,single_review["rating"]]
            
            # Update the weighted avg for all items in the review
            for key in running_total.keys():
                running_total[key][0] = self.get_weighted_average(float(review_rating), running_total[key][0]) 

        final_list['food_ratings'] = running_total
        # print('FINAL LIST NO PROCESSING:', final_list)
        return(self.return_top_food_items(final_list))
 
    def get_sentiment(self, sentence):
        '''
        Input: Sentence we want the sentiment for
        Output: Returns the sentiment of the sentence
        '''
        return TextBlob(sentence).sentiment.polarity

    def get_weighted_average(self, review_rating, sentiment):
        '''
        Input: review_rating, and sentiment score
        Output: Returns the weighted average of the review rating and the sentiment score
        '''
        # Normalize the review rating between -1 and 1 
        normalized_review_rating = 2*((review_rating - 1)/(5-1))-1 # Formula: 2 * ((x - min(x))/(max(x)-max(x)))-1
        
        # Multiply by the respective weights and return the weighted average
        return (self.sentence_weight * sentiment) + (self.review_weight * normalized_review_rating) 

    def return_top_food_items(self, final_list):
        '''
        Input: Final list with the food items and their corresponding ratings
        Output: Food items along with their sentiment and counts
        '''
        chrome_returned_json = {"food_items": {} }
        chrome_returned_json['restaurant_name'] = final_list['restaurant_name']

        # Find max number of identified words for a single food item
        max_count = max([val[1] for val in final_list['food_ratings'].values()])

        # print("\nCLEANING THRESHOLDS")
        # Check if number of times a food is identified is greater than a threshold
        for key,value in final_list['food_ratings'].items():
            if value[1] > math.ceil(self.threshold * max_count):
                chrome_returned_json['food_items'][key] = value
        return chrome_returned_json
        
if __name__ == '__main__':
    test = Sentiment(0.5,0.5, 0.2).calculate_final_json()
    print(test)
