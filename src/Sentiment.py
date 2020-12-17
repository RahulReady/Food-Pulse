# Get rid of comments for prod?

# Confused that pylint is throwing an error, but it works!? LOOK INTO THIS
from NER import NER
import pandas as pd
import spacy
import json
import spacy.displacy as displacy
from textblob import TextBlob
import os
from nltk.tokenize import sent_tokenize, word_tokenize

# print(os.getcwd())


class Sentiment(NER):
    '''
    Input: None
    Output: Class for returning the X best/worst food items.
    #TODO
    [X] Read in json file 
    [X] Split sentences and then select sentences that contain the identified words
    [X] Find sentiment of those sentences
    [X] Take a weighted average of sentiment and rating score
    [] Return the top/worst 3 items


    @Notes
    1) Given a set of possible food items and it's review scores, how do we determine what to finally use?
    Set a min number of items to be detected? Would this scale based on total reviews?
    CHECK IF IDENTIFIED WORD IS BLANK AND REMOVE IT
    '''

    def __init__(self, sentence_weight, review_weight, threshold):
        self.path = self.get_restaurant_review_path()
        self.sentence_weight = sentence_weight
        self.review_weight = review_weight
        self.threshold = threshold

    def sentences_with_identified_words(self):
        '''
        Input: None
        Output: Returns the final json that contains the food rating sentiment for each identified food word
        '''
        # Read in json file
        with open(self.path, 'r') as f:
            contents = json.load(f)
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
                        for food_item in single_review['identified_foods']:
                            if food_item in sent:
                                if food_item in running_total:
                                    # Update sentiment, count
                                    combined_review_rating = self.get_weighted_average(float(review_rating), float(self.get_sentiment(sent)))
                                    running_total[food_item][0] = running_total[food_item][0] + combined_review_rating
                                    running_total[food_item][1] = running_total[food_item][1] + 1
                                else:
                                    # Initialize sentiment, count 
                                    combined_review_rating = self.get_weighted_average(float(review_rating), float(self.get_sentiment(sent))) 
                                    running_total[food_item] = [combined_review_rating, 1]

        final_list['food_ratings'] = running_total
        self.return_best_worst_items(final_list)
 
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
        # Need to normalize the review rating between -1 and 1 (Would probably be slightly faster to just make this a hash table?) 
        normalized_review_rating = 2*((review_rating - 1)/(5-1))-1 # Formula: 2 * ((x - min(x))/(max(x)-max(x)))-1
        
        # Multiply by the respective weights and return the weighted average
        return (self.sentence_weight*sentiment) + (self.review_weight*normalized_review_rating) 

    def return_best_worst_items(self, final_list):
        '''
        Input: Final list with the food items and their corresponding ratings
        Output: Top/worst food items
        '''
 
        # print(final_list)
        chrome_returned_json = {'food_items': {}}
        chrome_returned_json['restaurant_name'] = final_list['restaurant_name']

        # Count max number of reviews and check if count > threshold?
        # Find max number of identified words for a single food item
        max_count = max([val[1] for val in final_list['food_ratings'].values()])
        
        # Check if number of times a food is identified is greater than a threshold
        for key,value in final_list['food_ratings'].items():
            if value[1] > (self.threshold * max_count):
                chrome_returned_json['food_items'][key] = value[0]/value[1]
        # print(chrome_returned_json)
        # del chrome_returned_json['food_items']
        print(chrome_returned_json)


    def main(self):
        '''
        Input: None
        Output: Runs this class
        '''
        self.sentences_with_identified_words()

        
if __name__ == '__main__':
    Sentiment(0.3,0.7, 0.2).main()
