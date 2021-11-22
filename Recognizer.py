### Phase I: Identification of serious games for kids

import json
import play_scraper
import pandas as pd
from google_play_scraper import app
import re

#Filter this dataset with all the educational and family-related categories + specific features
def filter(df):
    df = df[((df["Category"] == "Education")
                 | (df["Category"] == "Educational")
                 | (df["Category"] == "Family")
                 | (df["Category"] == "Learn")
                 | (df["Category"] == "4 year old kids")
                 | (df["Category"] == "4 year olds"))
                & (df["Rating"] >= 4) #lower it
                & (df["Rating Count"] >= 50000)] #lower it
    return df #goal size = 1000 < x < 2000


##select only the apps from the dataset that are games
def select_games(df):
    problematic_apps = []
    not_games = []
    for i in range(len(df)):
        try:
            app_edu = app(df.iloc[i]["App Id"])
            json_app_edu = json.dumps(app_edu)
            json_app_edu = json.loads(json_app_edu)
            cat_app = json_app_edu["genreId"]
            if cat_app[:4] != "GAME":
                not_games.append(i)
        except:
            #print(i)
            problematic_apps.append(i)
            continue
    df = df.drop(index=problematic_apps, axis=0)
    df_g = df.drop(index=not_games, axis=0)
    return df_g

##delete the apps without a clear age range nor learning category
def filter_non_enrichable(df):
    df = df[((df["Learning_category"] != "")
                 & (df["Age_range"] != ""))]
    return df

## enrich the dataset
def enrich_dataframe(df):
    desc_app = []
    rev_app = []
    for i in range(len(df)):
        app_edu = app(df.iloc[i]["App Id"])
        json_app_edu = json.dumps(app_edu)
        json_app_edu = json.loads(json_app_edu)
        desc = json_app_edu["description"]
        rev = json_app_edu["reviews"]
        desc_app.append(desc)
        rev_app.append(rev)
    df["Description"] = desc_app
    df["Reviews"] = rev_app
    return df


## Use of NLP to enrich the dataset with more detailed features



def find_lc(df):
    # Complete learning category
    # List of learning categories
    learning_cat = ["science", "counting", "language", "creativity", "shape", "food", "music", "sport"]
    # List of keywords per category
    science = ["science", "nature", "physics", "chemistry", "biology", "mathematics", "plants", "informatics",
               "programming", "star", "planet", "galaxy", "scientific", "robot", "life", "laboratory", "virus"]
    counting = ["counting", "number", "addition", "substraction", "division", "multiplication", "add", "fraction",
                "mathematics", "sum", "product"]
    language = ["language", "english", "spanish", "chinese", "vocabulary", "writing", "reading", "grammar"
                                                                                                 "translation",
                "linguistic", "speech", "slang", "mother tongue", "billingual", "latin"]
    creativity = ["creativity", "drawing", "color", "design", "imagination", "idea", "painting", "pencil", "artist"]
    shape = ["shape", "triangle", "rectangle", "square", "round", "circle", "cube", "sphere", "icon"]
    food = ["food", "health", "nutrition", "ingredients", "cook", "meal", "vegetable", "fruit", "meat", "drink"]
    music = ["music", "instrument", "compose", "sound", "partition", "lyric", "song", "dance", "concert",
             "soundtrack", "MP3", "folk", "rock", "hip hop", "jazz", "pop", "echo"]
    sport = ["sport", "ball", "run", "coach", "score", "train", "team", "shot"]

    # List of all keywords combined
    keywords_cat = [science, counting, language, creativity, shape, food, music, sport]
    lc = []
    for i in range(len(df)):
        desc = df.iloc[i]["Description"]
        Mx = 0
        cat = ""
        for j in range(len(keywords_cat)):
            m = 0
            nb = []
            for k in range(len(keywords_cat[j])):
                nb.append(desc.count(keywords_cat[j][k]))
            m = max(nb)
            if m > Mx:
                Mx = m
                cat = learning_cat[j]
        lc.append(cat)
    df["Learning_category"] = lc
    return df




def find_age_range(df):
    # Complete the age range
    # List of age ranges
    age_range = ["babies", "children", "adolescents", "adults"]
    # List of keywords per category
    babies = ["baby", "babies", "1 year-old", "2 year-old", "3 year-old", "infant", "newborn",
              "nursery"]  # 0-3 year-old
    children = ["child", "children", "kid", "4 year-old", "5 year-old", "6 year-old", "7 year-old", "8 year-old",
                "9 year-old", "10 year-old", "11 year-old", "12 year-old", "toddler", "elementary school",
                "childhood", "preschool"]  # 4-12 year-old
    adolescents = ["teenage", "adolescent", "middle school", "highschool", "13 year-old", "14 year-old", "15 year-old",
                   "16 year-old", "17 year-old", "18 year-old", "19 year-old"]  # 13-19 year-old
    adults = ["adult", "student", "university", "old", "middle-aged", "20 year-old", "mature",
              "grown-up", "majority"]  # 20 and more year-old

    # List of all keywords combined
    keywords_age = [babies, children, adolescents, adults]
    ar = []
    for i in range(len(df)):
        desc = df.iloc[i]["Description"]
        Mx = 0
        age = ""
        for j in range(len(keywords_age)):
            m = 0
            nb = []
            for k in range(len(keywords_age[j])):
                nb.append(desc.count(keywords_age[j][k]))
            m = max(nb)
            if m > Mx:
                Mx = m
                age = age_range[j]
        ar.append(age)
    df["Age_range"] = ar
    return df


def main():
    print("Reading the input")
    print("")
    df = pd.read_csv(r'Sources/Google-Playstore.csv')
    # Filtering the dataset with educational apps respecting specific features
    df_edu = filter(df)
    # The dataset now only contains specific lines and has an index composed of the remaining rows' numbers
    # Reinitialisation of the index to be [0,1,...,n]
    df_edu = df_edu.set_index([pd.Index([i for i in range(len(df_edu))])])
    # Selecting the educational games
    df_edu_g = select_games(df_edu)
    df_edu_g = df_edu_g.set_index([pd.Index([i for i in range(len(df_edu_g))])])
    # Improving the dataset
    # Add descriptions, number of reviews
    df_edu_g = enrich_dataframe(df_edu_g)
    # Use of NLP to add learning categories and age ranges
    df_edu_g = find_lc(df_edu_g)
    df_edu_g = find_age_range(df_edu_g)
    df_edu_g = filter_non_enrichable(df_edu_g)
    print(df_edu_g)
    df_edu_g.to_csv(r'dataset_seriousgames.csv', index=False)

main()


#BUILDING DATABASE WITH TINYDB
#FROM CSV TO JSON

#df.to_json (r'path where the JSON file will be stored\JSON name file.json')

#from tinydb import TinyDB, Query
#db = TinyDB('path of the json file.json')
#document = Query()
#for app in db:
# print(app)
# print(app['appName'])
#
#print(db.get(document.appID == 'some app id')) it will return just one docuemnt, the match
#print(db.search(document.score > 4)) it will return an ARRAY of documents

#from pymed import PubMed
#pubmed = PubMed(tool='name_of_the_database', email='simonecensuales1998@gmail.com')

#results = pubmed.query('App Name', max_results = 50) (?)
#results = pubmed.query(App Name, max_results = 50) (?)
#||
#\/
#papers = []
#for res in results:
#   papers.append(res.toDict())
#THE ISSUE HERE IS THAT WE WILL HAVE ALL THE PAPERS TOGETHER
#SO WE NEED TO FIND A WAY TO DISTINGUISH THE PAPERS OF EACH APPLICATIONS
#MAYBE USING A DOUBLE LIST?

#or

#papersInPubMed = [][]
#for app in db:
#   result = pubmed.query('app['App Name']', max_results = 50)
#   for res in result:
#       papersInPubMed[res].append(res.toDict())

#then we have to decide if the papers will be merged in our database
#or
#we can build another database concerning only the publictions and the 
#pubmed id of the application
