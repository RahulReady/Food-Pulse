
#Todo
# [] Figure out importing and reorg project structure
# https://stackoverflow.com/questions/37233140/python-module-not-found

# Assuming the cwd is the ~/Chrome_Extension_Agg_App ********** Have to possibly set the working directory when we dockerize this
# Not sure if the following is needed?
# sys.path.insert(0, os.getcwd())

# General Imports
import sys, os # Useful directory imports
import importlib # Needed for testing changes to code

# Custom Imports
from Processing_Pipeline.NLP import NLP_script
from Processing_Pipeline.Scraping_reviews import scraping_reviews

# Following code needed if the Processing Pipeline scripts are updated
importlib.reload(NLP_script)
importlib.reload(scraping_reviews)


print(NLP_script.test())
print(scraping_reviews.test1())


if __name__ == "__main__":


    # Each month
    '''
    updateALL()
    createALLScores()
    '''
    # a = test()
    # print(a)
