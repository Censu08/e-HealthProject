import json
import pandas as pd
from google_play_scraper import app
# from tinydb import Query
from pymed import PubMed


# Filter this dataset with all the educational and family-related categories + specific features
def game_filter(df):
    df = df[((df["Category"] == "Education")
             | (df["Category"] == "Educational")
             | (df["Category"] == "Family")
             | (df["Category"] == "Learn")
             | (df["Category"] == "4 year old kids")
             | (df["Category"] == "4 year olds"))
            & (df["Rating"] >= 4.5)  # lower it
            & (df["Rating Count"] >= 50000)]  # lower it
    return df  # goal size = 1000 < x < 2000


# select only the apps from the dataset that are games
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


def search_keyword(mega_string):
    points = 0
    with open('../Sources/Studies/CaseControl.txt') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in mega_string:
                points = points + 4
                break
    with open('../Sources/Studies/CaseSeries.txt') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in mega_string:
                points = points + 2
                break
    with open('../Sources/Studies/CohortStudy.txt') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in mega_string:
                points = points + 5
                break
    with open('../Sources/Studies/MetaAnalysis.txt') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in mega_string:
                points = points + 7
                break
    with open('../Sources/Studies/ObservationalStudy.txt') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in mega_string:
                points = points + 3
                break
    with open('../Sources/Studies/Other.txt') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in mega_string:
                points = points + 1
                break
    with open('../Sources/Studies/RCT.txt') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in mega_string:
                points = points + 6
                break
    with open('../Sources/Studies/SystematicReview.txt') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in mega_string:
                points = points + 7
                break
    return points


# some papers dont have conclusions or results
def meta_paper_creator(app_documented):
    result = ""
    for paper in app_documented[1]:
        str1 = paper['title']
        if str1 is None:
            str1 = ""
        str2 = paper['abstract']
        if str2 is None:
            str2 = ""
        str3 = ""
        for keyword in paper['keywords']:
            if keyword is not None:
                str3 = str3 + keyword + " "
        str4 = paper['journal']
        if str4 is None:
            str4 = ""
        str5 = paper['conclusions']
        if str5 is None:
            str5 = ""
        str6 = paper['results']
        if str6 is None:
            str6 = ""
        result = result + str1 + str2 + str3 + str4 + str5 + str6
    return result


def validate(level):
    if level >= 3:
        return True
    else:
        return False


def pubmed_search(query_keyword):
    pubmed = PubMed(tool='name_of_the_database', email='simonecensuales1998@gmail.com')
    results = pubmed.query(query_keyword, max_results=2)  # query_keyword in AND con game
    papers = []
    for res in results:
        papers.append(res.toDict())
    return papers


def build_database(df_edu_g):
    df_edu_g.to_json(r'dataset_serious_games.json')
    # db = TinyDB('dataset_serious_games.json')
    app_documented = []
    for application in df_edu_g['App Name']:
        app_documented.append([application, pubmed_search(application)])
    return app_documented


def real_validator():
    df = pd.read_csv(r'Outputs/dataset_serious_games.csv')
    app_documented = build_database(df)
    for x in app_documented:
        mega_string = meta_paper_creator(x)
        app_validation_level = search_keyword(mega_string)
        validation = validate(app_validation_level)
        print(validation)
    app_doc = pd.Dataframe(app_documented)
    app_doc.to_csv("dataset_papers.csv", index=False)

def read_serious_games():
    print("Reading the input")
    print("")
    df = pd.read_csv(r'../Sources/Google-Playstore.csv')
    # Filtering the dataset with educational apps respecting specific features
    df_edu = game_filter(df)
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
    df_edu_g = filter_non_reachable(df_edu_g)
    print(df_edu_g)
    df_edu_g.to_csv(r'/Outputs/dataset_serious_games.csv', index=False)


def print_dashboard():
    print("ueeeeeeeeeeeeee")
