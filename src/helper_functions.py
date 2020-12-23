import os
    
def get_restaurant_review_path():
    '''
    Input: None 
    Output: Return the location of the restaurant reviews
    '''
    return (os.getcwd() + '/src/entity/scrapped_restaurant_reviews/restaurant.json')