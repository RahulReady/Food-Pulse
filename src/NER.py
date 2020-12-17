# Get rid of comments for prod?
import spacy
#import spacy.displacy as displacy
import os
import json
import string



class NER:
    '''
    Class that takes in the reviews (json) and modifies the scraped restaurant json, adding the NER model's recognized food words.
    @Future
    1) NeuroNER would be interesting to look into
    '''
    

    def __init__(self, test):
        self.model = self.spacy_model_setup()
        self.test = test

    def spacy_model_setup(self):
        '''
        Input: None
        Returns: loaded spacy model to be used for NER
        '''
        model_location = os.getcwd() + '/src/entity/output_dir'
        loaded_model = spacy.load(model_location)  

        # testing to check the model location
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
        test = self.test
        all_recognized_words = []
        
        with open(json_file_path, 'r') as f:
            contents = json.load(f)
            for ind, val in enumerate(contents['reviews']):
                review_recognized_words = []
                # Recognize words  (add displacy???? to test??)
                # Use the model on the reviews
                doc = model(val['review'])

                # Recognized words
                if test:
                    # Show the model output
                    [all_recognized_words.append(ent.text.lower().translate(str.maketrans('', '', string.punctuation))) for ent in doc.ents] 

                # Append the words 
                [review_recognized_words.append(ent.text.lower().translate(str.maketrans('', '', string.punctuation))) for ent in doc.ents]

                # print('Entities', [review_recognized_words.append(ent.text.lower().translate(str.maketrans('', '', string.punctuation))) for ent in doc.ents])
                contents['reviews'][ind]['identified_foods'] = review_recognized_words


        # Writing the relevant information to the existing restaurant.json file
        with open(json_file_path, 'w') as outfile:  
            json.dump(contents, outfile) 
        
        # Printing counts of the words that the model recognizes
        if test:
            cnts = {} 
            for val in all_recognized_words:
                if val in cnts:
                    cnts[val] = cnts[val] + 1
                else:
                    cnts[val] = 1
            print(cnts)

    def main(self):
        '''
        Input: None
        Output: Runs this class
        '''
        self.recognize_words()


if __name__ == '__main__':
    NER(True).main()