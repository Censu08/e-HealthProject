### Phase I: Identification of serious games for kids

## Step 0: Importation of the libraries

import json
import play_scraper
import pandas as pd
from google_play_scraper import app
import re

# Preliminary function
def isascii(s):
    """Check if the characters in string s are in ASCII, U+0-U+7F."""
    return len(s) == len(s.str.encode(encoding = 'raw_unicode_escape'))

## Step 1: Filter this dataset with all the educational and family-related categories + specific features

def filter(df):
    # and = &, not = ~, or = |
    df_edu = df[((df["Category"] == "Education")
                 | (df["Category"] == "Educational")
                 | (df["Category"] == "Family")
                 | (df["Category"] == "Learn")
                 | (df["Category"] == "4 year old kids")
                 | (df["Category"] == "4 year olds"))
                & (df["Rating"] >= 4.8)
                & (df["Rating Count"] >= 1000)
                & (df["Minimum Installs"] >= 1000000)
                & (isascii(df["App Name"]))]
    return df_edu

## Step 2: Use of google-play-scraper to select only the apps from the dataset that are games

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
            print(i)
            problematic_apps.append(i)
            continue
    df = df.drop(index=problematic_apps, axis=0)
    df_g = df.drop(index=not_games, axis=0)
    return df_g

## Step 3: Use of google-play-scraper to enrich the dataset

# Complete description, reviews with google-play-scraper
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


## Step 4: Use of NLP to enrich the dataset with more detailed features

# Complete learning category
# List of learning categories
learning_cat = ["science", "counting", "language", "creativity", "shape", "food", "music", "sport"]
# List of keywords per category
science = ["science", "nature", "physics", "chemistry", "biology", "mathematics", "plants", "informatics",
                    "programming", "star", "planet", "galaxy", "scientific", "robot", "life", "laboratory", "virus"]
counting = ["counting", "number", "addition", "substraction", "division", "multiplication", "add", "fraction",
                     "mathematics", "sum", "product"]
language = ["language", "english", "spanish", "chinese", "vocabulary", "writing", "reading", "grammar"
                     "translation", "linguistic", "speech", "slang", "mother tongue", "billingual", "latin"]
creativity = ["creativity", "drawing", "color", "design", "imagination", "idea", "painting", "pencil", "artist"]
shape = ["shape", "triangle", "rectangle", "square", "round", "circle", "cube", "sphere", "icon"]
food = ["food", "health", "nutrition", "ingredients", "cook", "meal", "vegetable", "fruit", "meat", "drink"]
music = ["music", "instrument", "compose", "sound", "partition", "lyric", "song", "dance", "concert",
                  "soundtrack", "MP3", "folk", "rock", "hip hop", "jazz", "pop", "echo"]
sport = ["sport", "ball", "run", "coach", "score", "train", "team", "shot"]

# List of all keywords combined
keywords_cat = [science, counting, language, creativity, shape, food, music, sport]

def find_lc(df, learning_cat, keywords_cat):
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

# Complete the age range
# List of age ranges
age_range = ["babies", "children", "adolescents", "adults"]
# List of keywords per category
babies = ["baby", "babies", "1 year-old", "2 year-old", "3 year-old", "infant", "newborn", "nursery"] # 0-3 year-old
children = ["child", "children", "kid", "4 year-old", "5 year-old", "6 year-old","7 year-old", "8 year-old",
            "9 year-old", "10 year-old", "11 year-old", "12 year-old", "toddler", "elementary school",
            "childhood", "preschool"] # 4-12 year-old
adolescents = ["teenage","adolescent", "middle school", "highschool", "13 year-old", "14 year-old", "15 year-old",
               "16 year-old", "17 year-old", "18 year-old", "19 year-old"] # 13-19 year-old
adults = ["adult", "student", "university", "old", "middle-aged", "20 year-old", "mature",
          "grown-up", "majority"] # 20 and more year-old

# List of all keywords combined
keywords_age = [babies, children, adolescents, adults]

def find_age_range(df, age_range, keywords_age):
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


## Step 5: Call all these functions

def main():
    df = pd.read_csv(r'C:\Users\Gilles FACCIN\Desktop\Polimi 2021-2022\E-HEALTH METHODS\PRACTICES\Google-Playstore.csv')
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
    df_edu_g = find_lc(df_edu_g, learning_cat, keywords_cat)
    df_edu_g = find_age_range(df_edu_g, age_range, keywords_age)
    print(df_edu_g)
    # df_edu_g.to_csv(r'updatedDB.csv', index=False)

main()

## Step 6: Evaluate the performance of the algorithm

# Accuracy, specificity, sensitivity
