### Phase I: Identification of serious games for kids

## Step 1: Importation of the libraries

import json
import play_scraper
import pandas as pd
from google_play_scraper import app

## Step 2: Download .csv dataset called Google-Playstore (main dataset of all Google PlayStore apps)

df = pd.read_csv(r'C:\Users\Gilles FACCIN\Desktop\Polimi 2021-2022\E-HEALTH METHODS\Practices\Google-Playstore.csv')

## Step 3: Filter this dataset with all the educational and family-related categories

def filter(df):
    # and = &, not = ~, or = |
    df_edu = df[(df["Category"] == "Education")
                | (df["Category"] == "Educational")
                | (df["Category"] == "Family")
                | (df["Category"] == "Learn")
                | (df["Category"] == "4 year old kids")
                | (df["Category"] == "4 year olds")]
    return df_edu

df_edu = filter(df)

# The dataset now contains only specific lines and has an index composed of the remaining rows' numbers
# Reinitialisation of the index to be [0,1,...,n]
df_edu = df_edu.set_index([pd.Index([i for i in range(len(df_edu))])])
print(df_edu)

## Step 4: Use of google-play-scraper to select only the apps from the dataset that are games

# Problem: some apps of the Google-Playstore.csv are not found in google-play-scraper
# Solution: Deleting them manually, line by line (very long)?
# df_edu = df_edu.drop(index=7,axis=0)
# df_edu = df_edu.set_index([pd.Index([i for i in range(len(df_edu))])])

def select_games(df):
    problematic_apps = []
    not_games = []
    for i in range(len(df)):
        try :
            app_edu = app(df.iloc[i]["App Id"])
            json_app_edu = json.dumps(app_edu)
            json_app_edu = json.loads(json_app_edu)
            cat_app = json_app_edu["genreId"]
            # print(app_edu)
            if cat_app[:4] != "GAME":
                not_games.append(i)
        except :
            print(i)
            problematic_apps.append(i)
            continue
    df = df.drop(index = problematic_apps, axis = 0)
    df_g = df.drop(index = not_games, axis = 0)
    return df_g

df_edu_g = select_games(df_edu)
print(df_edu_g)

# ## Step 5: Use of google-play-scraper and play-scraper to enrich the dataset
#
# # Add some new columns, for now only containing 0: description, learning category, expert validation, reviews
# df_edu_g = df_edu_g.assign(Description = 0, Learning_category = 0, Expert_validation = 0, Reviews = 0, Age_range = 0)
#
# # Complete description, reviews (and learning category?) with google-play-scraper
# def enrich_dataframe(df):
#     for i in range(len(df)):
#         app_edu = app(df.iloc[i]["App Id"])
#         json_app_edu = json.dumps(app_edu)
#         json_app_edu = json.loads(json_app_edu)
#         desc_app = json_app_edu["description"]
#         df.iloc[i]["Description"] = desc_app
#         # lc_app = json_app_edu["familyGenre"]
#         # df.iloc[i]["Learning_category"] = lc_app
#         rev_app = json_app_edu["reviews"]
#         df.iloc[i]["Reviews"] = rev_app
#         # print(i)
#     return df
#
# df_edu_g = enrich_dataframe(df_edu_g)
# print(df_edu_g)

# What about learning category and expert validation?

## Step 6: Clean the dataset

##----------------------------------------------------------------------------------------------------------------------

## Phase IIa: Characterisation of relevant serious games

# Extract information from the PUBMED webpages

# Select relevant publications and create database out of them

# Characterise publications - identify relevant information from the texts
