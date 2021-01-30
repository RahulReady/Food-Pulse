# from helper_functions import get_restaurant_review_path
import spacy
import os
import json
import string
from nltk.stem.snowball import SnowballStemmer

class NER: 
    def __init__(self, reviews, test_output):
        self.model = self.spacy_model_setup()
        self.reviews = reviews
        self.test_output = test_output
        self.stemmer = SnowballStemmer("english")

    def spacy_model_setup(self):
        '''
        Input: None
        Returns: loaded spacy model to be used for NER
        '''
        model_location = os.getcwd() + '/src/entity/output_dir'
        loaded_model = spacy.load(model_location)  

        # Log the model location
        # print("Loaded model '%s'" % model_location)
        return loaded_model

    def recognize_words(self):
        '''
        Input: None 
        Output: Return the modified json to be sent for sentiment analysis
        '''
        # json_file_path = get_restaurant_review_path()
        model = self.model
        test_output = self.test_output
        all_recognized_words = []
        
        # with open(json_file_path, 'r') as f:
        # contents = json.load(f)
        contents = self.reviews
        for ind, val in enumerate(contents['reviews']):
            review_recognized_words = []
            # Use the model on the reviews
            doc = model(val['review'])

            # Recognized words (don't add words that are less than or equal to 3 chars)
            if test_output: # log the output if testing the outputs
                [1 if len(ent.text)<=3 else all_recognized_words.append(ent.text.lower().translate(str.maketrans('', '', string.punctuation))) for ent in doc.ents ]

            # Append the words 
            [1 if len(ent.text)<=3 else review_recognized_words.append(self.stemmer.stem(ent.text.lower().translate(str.maketrans('', '', string.punctuation)))) for ent in doc.ents ]
            
            # Add the words to the json
            contents['reviews'][ind]['identified_foods'] = review_recognized_words
        return contents
        # # Writing the relevant information to the existing restaurant.json file
        # json_file_path =  json_file_path
        # with open(json_file_path, 'w') as outfile:  
        # # local with open(json_file_path, 'w') as outfile:  
        #     json.dump(contents, outfile) 
        
        # Printing counts of the words that the model recognizes
        if test_output:
            cnts = {} 
            for val in all_recognized_words:
                if val in cnts:
                    cnts[val] = cnts[val] + 1
                else:
                    cnts[val] = 1
            print(cnts)

if __name__ == '__main__':

    # NER(True).recognize_words()
    stemmer = SnowballStemmer("english")
    # # stemmer = PorterStemmer()
    plurals = ["fried rice", 'rice', 'burgers', 'sandwiches', 'nuggets']
    # # print([stemmer.stem(plural) for plural in plurals])
    print([stemmer.stem(plural) for plural in plurals])