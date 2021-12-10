import pandas as pd
from pymed import PubMed
from random import *

from Library.Recognizer import ROOT_DIR


def search_keyword(mega_string):
    if len(mega_string) < 1:
        return 0
    points = 0
    with open(ROOT_DIR + '/Sources/Studies/CaseControl.txt') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in mega_string:
                points = points + 4
                break
    with open(ROOT_DIR + '/Sources/Studies/CaseSeries.txt') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in mega_string:
                points = points + 2
                break
    with open(ROOT_DIR + '/Sources/Studies/CohortStudy.txt') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in mega_string:
                points = points + 5
                break
    with open(ROOT_DIR + '/Sources/Studies/MetaAnalysis.txt') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in mega_string:
                points = points + 7
                break
    with open(ROOT_DIR + '/Sources/Studies/ObservationalStudy.txt') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in mega_string:
                points = points + 3
                break
    with open(ROOT_DIR + '/Sources/Studies/Other.txt') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in mega_string:
                points = points + 1
                break
    with open(ROOT_DIR + '/Sources/Studies/RCT.txt') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in mega_string:
                points = points + 6
                break
    with open(ROOT_DIR + '/Sources/Studies/SystematicReview.txt') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in mega_string:
                points = points + 7
                break
    return points


# return megastring
def meta_paper_creator(app_documented):
    mega_string = ""
    for paper in app_documented[len(app_documented) - 1]:
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
        mega_string = mega_string + str1 + str2 + str3 + str4 + str5 + str6
    return mega_string


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


def build_database(df):
    app_documented = []
    for i in range(len(df)):
        app_documented.append(
            [df.iloc[i]["App Name"], df.iloc[i]["Learning_category"], pubmed_search(df.iloc[i]["App Name"])])
    return app_documented


def validation_level_calculator(app_documented):
    mega_string = meta_paper_creator(app_documented)
    app_validation_level = search_keyword(mega_string)
    return app_validation_level


def app_to_documented_app(app_name):
    return [app_name, pubmed_search(app_name)]


def similarity_function_list(non_validated_apps, validated_app):
    for applicazione in non_validated_apps:
        similarity_function(applicazione, validated_app)


def similarity_function(non_validated_application, validated_app):
    learning_category = non_validated_application[1]
    shuffle(validated_app)
    suggested_apps = []
    for x in validated_app:
        if len(suggested_apps) == 3:
            break
        if x[1] == learning_category:
            suggested_apps.append(x[0])
    print(suggested_apps)


def single_app_validation_level(app_name):
    return validation_level_calculator(app_to_documented_app(app_name))


def real_validator():
    df = pd.read_csv(r"" + ROOT_DIR + '/Outputs/dataset_serious_games.csv')
    app_documented = build_database(df)
    non_validated_apps = []
    validated_app = []
    for x in app_documented:
        app_validation_level = validation_level_calculator(x)
        validation = validate(app_validation_level)
        if validation:
            validated_app.append(x)
        else:
            non_validated_apps.append(x)
        print(validation)
    similarity_function_list(non_validated_apps, validated_app)
    app_doc = pd.DataFrame(app_documented)
    app_doc.to_csv(ROOT_DIR + "/Outputs/dataset_papers.csv", index=False)
