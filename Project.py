import json
import play_scraper
import pandas as pd
from google_play_scraper import app

import re

#TODO
def isascii(s):
    """Check if the characters in string s are in ASCII, U+0-U+7F."""
    return len(s) == len(s.str.encode(encoding = 'raw_unicode_escape'))

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
                & (isascii(df["App Name"]))

                ]
    return df_edu


def enrich_dataframe(df):
    df = df.assign(Description=0, Learning_category=0, Expert_validation=0, Reviews=0, Age_range=0)
    for i in range(len(df)):
        app_edu = app(df.iloc[i]["App Id"])
        json_app_edu = json.dumps(app_edu)
        json_app_edu = json.loads(json_app_edu)
        desc_app = json_app_edu["description"]
        df.iloc[i]["Description"] = desc_app
        rev_app = json_app_edu["reviews"]
        df.iloc[i]["Reviews"] = rev_app
    return df

# Complete learning category

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
keywords_lc = [science, counting, language, creativity, shape, food, music, sport]

def find_lc(df, keywords_lc):
    for i in range(len(df)):
        app_edu = app(df.iloc[i]["App Id"])
        json_app_edu = json.dumps(app_edu)
        json_app_edu = json.loads(json_app_edu)
        desc_app = json_app_edu["description"]
        Mx = 0
        cat = ""
        for j in range(len(keywords_lc)):
            nb = []
            for k in range(len(keywords_lc[j])):
                nb.append(desc_app.count(keywords_lc[j][k]))
                m = max(nb)
                if m > Mx:
                    Mx = m
                    cat = keywords[j]
        df.iloc[i]["Learning_category"] = cat
    return df


def main():
    df = pd.read_csv(r'Google-Playstore.csv')
    df_edu = filter(df)
    df_edu = df_edu.set_index([pd.Index([i for i in range(len(df_edu))])])
    df_edu_g = select_games(df_edu)
    df_edu_g = enrich_dataframe(df_edu_g)
    #df_edu_g = find_lc(df_edu_g)
    print(df_edu_g)
    #df_edu_g.to_csv(r'updatedDB.csv', index=False)


main()



## Phase IIa: Characterisation of relevant serious games

# Extract information from the PUBMED webpages

# Select relevant publications and create database out of them

# Characterise publications - identify relevant information from the texts


# accuracy
