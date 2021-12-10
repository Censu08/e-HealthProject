import json
import pandas as pd
from google_play_scraper import app
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Filter this dataset with all the educational and family-related categories + specific features
def game_filter(df):
    df = df[((df["Category"] == "Education")
             | (df["Category"] == "Educational")
             | (df["Category"] == "Family")
             | (df["Category"] == "Learn")
             | (df["Category"] == "4 year old kids")
             | (df["Category"] == "4 year olds"))
            & (df["Rating"] >= 4)  # lower it
            & (df["Rating Count"] >= 20000)]  # lower it
    # & (df["Rating Count"] >= 50000)]  # lower it
    return df  # goal size = 1000 < app_name < 2000


# select only the apps from the dataset that are games
def select_games(df):
    problematic_apps = []
    not_games = []
    for i in range(len(df)):
        try:
            app_edu = app(df.iloc[i]["App Id"])
            json_app_edu = json.dumps(app_edu)
            json_app_edu = json.loads(json_app_edu)
            genre = json_app_edu["genreId"]
            title = json_app_edu["title"]
            description = json_app_edu["description"]
            if "Game" not in json_app_edu["title"] and \
                    "Game" not in json_app_edu["description"] and \
                    "game" not in json_app_edu["description"] and \
                    json_app_edu["genreId"][:4] != "GAME":
                not_games.append(i)
        except (Exception,):
            problematic_apps.append(i)
            continue
    df = df.drop(index=problematic_apps, axis=0)
    df_g = df.drop(index=not_games, axis=0)
    return df_g


# delete the apps without a clear age range nor learning category
def filter_non_reachable(df):
    df = df[((df["Learning_category"] != "")
             & (df["Age_range"] != ""))]
    return df


# enrich the dataset
def enrich_dataframe(df):
    desc_app = []
    rev_app = []
    for i in range(len(df)):
        app_edu = app(df.iloc[i]["App Id"])
        json_app_edu = json.dumps(app_edu)
        json_app_edu = json.loads(json_app_edu)
        desc = json_app_edu["description"]
        rev = json_app_edu["reviews"]
        # validation_level = validation_level_calculator(([df.iloc[i]["App Name"], [], pubmed_search(df.iloc[i]["App Name"])]))
        desc_app.append(desc)
        rev_app.append(rev)
    df["Description"] = desc_app
    df["Reviews"] = rev_app
    return df


# Use of NLP to enrich the dataset with more detailed features
def finder(df, keywords, learning_cat):
    lc = []
    for i in range(len(df)):
        desc = df.iloc[i]["Description"]
        mx = 0
        cat = ""
        for j in range(len(keywords)):
            nb = []
            for k in range(len(keywords[j])):
                nb.append(desc.count(keywords[j][k]))
            m = max(nb)
            if m > mx:
                mx = m
                cat = learning_cat[j]
        lc.append(cat)
    return lc


def find_lc(df):
    # Complete learning category
    # List of learning categories
    learning_cat = ["science", "counting", "language", "creativity", "shape", "food", "music", "sport"]
    # List of keywords per category
    science = ["science", "nature", "physics", "chemistry", "biology", "mathematics", "plants", "informatics",
               "programming", "star", "planet", "galaxy", "scientific", "robot", "life", "laboratory", "virus"]
    counting = ["counting", "number", "addition", "subtraction", "division", "multiplication", "add", "fraction",
                "mathematics", "sum", "product"]
    language = ["language", "english", "spanish", "chinese", "vocabulary", "writing", "reading", "grammar"
                                                                                                 "translation",
                "linguistic", "speech", "slang", "mother tongue", "bilingual", "latin"]
    creativity = ["creativity", "drawing", "color", "design", "imagination", "idea", "painting", "pencil", "artist"]
    shape = ["shape", "triangle", "rectangle", "square", "round", "circle", "cube", "sphere", "icon"]
    food = ["food", "health", "nutrition", "ingredients", "cook", "meal", "vegetable", "fruit", "meat", "drink"]
    music = ["music", "instrument", "compose", "sound", "partition", "lyric", "song", "dance", "concert",
             "soundtrack", "MP3", "folk", "rock", "hip hop", "jazz", "pop", "echo"]
    sport = ["sport", "ball", "run", "coach", "score", "train", "team", "shot"]

    # List of all keywords combined
    keywords = [science, counting, language, creativity, shape, food, music, sport]
    df["Learning_category"] = finder(df, keywords, learning_cat)
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
    adolescents = ["teenage", "adolescent", "middle school", "high school", "13 year-old", "14 year-old", "15 year-old",
                   "16 year-old", "17 year-old", "18 year-old", "19 year-old"]  # 13-19 year-old
    adults = ["adult", "student", "university", "old", "middle-aged", "20 year-old", "mature",
              "grown-up", "majority"]  # 20 and more year-old

    # List of all keywords combined
    keywords = [babies, children, adolescents, adults]
    df["Age_range"] = finder(df, keywords, age_range)
    return df


def import_df():
    df = pd.read_csv(r"" + ROOT_DIR + '/Sources/Google-Playstore.csv')
    # Filtering the dataset with educational apps respecting specific features
    df_edu = game_filter(df)
    # The dataset now only contains specific lines and has an index composed of the remaining rows' numbers
    # Reinitialisation of the index to be [0,1,...,n]
    df_edu = df_edu.set_index([pd.Index([i for i in range(len(df_edu))])])
    # Selecting the educational games
    df_edu_g = select_games(df_edu)
    df_edu_g = df_edu_g.set_index([pd.Index([i for i in range(len(df_edu_g))])])
    df_edu_g.to_csv(ROOT_DIR + "/Outputs/df_edu_g.csv", index=False)


def read_serious_games():
    df_edu_g = pd.read_csv(r"" + ROOT_DIR + '/Outputs/df_edu_g.csv')
    # Improving the dataset
    # Add descriptions, number of reviews
    df_edu_g = enrich_dataframe(df_edu_g)
    # Use of NLP to add learning categories and age ranges
    df_edu_g = find_lc(df_edu_g)
    df_edu_g = find_age_range(df_edu_g)
    df_edu_g = filter_non_reachable(df_edu_g)
    print(df_edu_g)
    df_edu_g.to_csv(r"" + ROOT_DIR + '/Outputs/dataset_serious_games.csv', index=False)
