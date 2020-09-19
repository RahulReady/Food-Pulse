

#Todo
# [] Set up venv and add chromedriver to that

# https://stackoverflow.com/questions/37233140/python-module-not-found

# General Imports
import sys, os # Useful directory imports
import importlib # Needed for testing changes to code
print(os.getcwd())

# Script Imports
from src.NLP_script import test10, test11
#from src.scraping_reviews import test1

# Following code needed if the Processing Pipeline scripts are updated
# importlib.reload(src.NLP_script)
# importlib.reload(src.scraping_reviews)


print(test10())
print(test11())







def lambda_handler(event, context):

  return{
    'body': event
  }


