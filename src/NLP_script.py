import pandas as pd
import spacy
import spacy.displacy as displacy




class NLP:
    #Fix after everything is done
    def __init__(self, df):
        self.df = df

    # def testing(self):
    #     return 'hello' + self.df


if __name__ == '__main__':


    # Starting as a df (Need to change later to get json data)
    # df = pd.read_csv('./src/review_data/reviews.csv')
    # print(df.head())
    df = 'yo'
    cl = NLP(df)

    nlp = spacy.load('en_core_web_md')
    doc = nlp('I love to eat chicken nuggets, tacos, burgers, pizza on a day to day basis in Chicago Illinois with Mark Zuckerburg')
    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)