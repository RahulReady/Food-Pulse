import spacy
import os
import json
import string

class NER:
    '''
    Class locates and modifies the restaurant json file (adding the NER model's recognized food words)
    '''
     
    def __init__(self, test_output):
        self.model = self.spacy_model_setup()
        self.test_output = test_output

    def spacy_model_setup(self):
        '''
        Input: None
        Returns: loaded spacy model to be used for NER
        '''
        model_location = os.getcwd() + '/src/entity/output_dir'
        loaded_model = spacy.load(model_location)  

        # Log the model location
        print("Loaded model '%s'" % model_location)
        return loaded_model

    def get_restaurant_review_path(self):
        '''
        Input: None 
        Output: Return the location of the restaurant reviews
        '''
        return (os.getcwd() + '/src/entity/scrapped_restaurant_reviews/restaurant.json')

    def recognize_words(self):
        '''
        Input: None 
        Output: Return the modified json to be sent for sentiment analysis
        '''
        json_file_path = self.get_restaurant_review_path()
        model = self.model
        test_output = self.test_output
        all_recognized_words = []
        
        with open(json_file_path, 'r') as f:
            contents = json.load(f)
            for ind, val in enumerate(contents['reviews']):
                review_recognized_words = []
                # Use the model on the reviews
                doc = model(val['review'])

                # Recognized words (don't add words that are less than or equal to 3 chars)
                if test_output: # log the output if testing the outputs
                    [1 if len(ent.text)<=3 else all_recognized_words.append(ent.text.lower().translate(str.maketrans('', '', string.punctuation))) for ent in doc.ents ]

                # Append the words 
                [1 if len(ent.text)<=3 else review_recognized_words.append(ent.text.lower().translate(str.maketrans('', '', string.punctuation))) for ent in doc.ents ]
                
                # Add the words to the json
                contents['reviews'][ind]['identified_foods'] = review_recognized_words

        # Writing the relevant information to the existing restaurant.json file
        with open(json_file_path, 'w') as outfile:  
            json.dump(contents, outfile) 
        
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

    NER(True).recognize_words()