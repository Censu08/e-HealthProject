import pandas as pd
from pymed import PubMed
from random import *
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
    app_name = non_validated_application[0]
    shuffle(validated_app)
    suggested_apps = []
    for x in validated_app:
        if len(suggested_apps) == 3:
            break
        if x[1] == learning_category:
            suggested_apps.append(x[0])
    print(suggested_apps)
    lst = list(zip(app_name, suggested_apps))
    sug = pd.DataFrame(lst, columns=['App Name', 'Suggested'])
    sug.to_csv(ROOT_DIR + "/Outputs/dataset_suggested.csv", index=False)


def single_app_validation_level(app_name):
    return validation_level_calculator(app_to_documented_app(app_name))


def real_validator():
    df = pd.read_csv(r"" + ROOT_DIR + '/Outputs/dataset_serious_games.csv')
    app_documented = build_database(df)
    # 2 df_2 = add_validation_column(app_documented)
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
    # df_2.to_csv(ROOT_DIR + "/Outputs/dataset_serious_final.csv", index=False)

def paper_search(app_name):
    pubmed = PubMed(tool='name_of_the_database', email='simonecensuales1998@gmail.com')
    results = pubmed.query(app_name, max_results=5)
    articleList = []
    articleInfo = []

    for article in results:
        # Print the type of object we've found (can be either PubMedBookArticle or PubMedArticle).
        # We need to convert it to dictionary with available function
        articleDict = article.toDict()
        articleList.append(articleDict)

    if len(articleList) != 0:
        # Generate list of dict records which will hold all article details that could be fetch from PUBMED API
        for article in articleList:
            # Sometimes article['pubmed_id'] contains list separated with comma - take first pubmedId in that list - thats article pubmedId
            pubmedId = article['pubmed_id'].partition('\n')[0]
            # Append article info to dictionary
            try:
                articleInfo.append({u'app_name': app_name,
                                    u'pubmed_id': pubmedId,
                                    u'title': article['title'],
                                    u'keywords': article['keywords'],
                                    u'journal': article['journal'],
                                    u'abstract': article['abstract'],
                                    u'conclusions': article['conclusions'],
                                    u'methods': article['methods'],
                                    u'results': article['results'],
                                    u'copyrights': article['copyrights'],
                                    u'doi': article['doi'],
                                    u'publication_date': article['publication_date'],
                                    u'authors': article['authors'],
                                    u'validation_level': single_app_validation_level(app_name)})
            except (Exception,):
                continue
    else:
        # Append article info to dictionary
        articleInfo.append({u'app_name': "",
                            u'pubmed_id': "",
                            u'title': "",
                            u'keywords': "",
                            u'journal': "",
                            u'abstract': "",
                            u'conclusions': "",
                            u'methods': "",
                            u'results': "",
                            u'copyrights': "",
                            u'doi': "",
                            u'publication_date': "",
                            u'authors': "",
                            u'validation_level': "0"})
    return articleInfo

# paper_search("English Listening and Speaking")

# def all_paper_search():
#     df = pd.read_csv(r"" + ROOT_DIR + '/Outputs/dataset_serious_games.csv')
#     articleInfo = paper_search(df.iloc[0]["App Name"])
#     # Generate Pandas DataFrame from list of dictionaries
#     articlesPD = pd.DataFrame.from_dict(articleInfo)
#     for i in range(1,len(df)):
#         print(i)
#         articleInfo = paper_search(df.iloc[i]["App Name"])
#         # Generate Pandas DataFrame from list of dictionaries
#         articlePD = pd.DataFrame.from_dict(articleInfo)
#         articlesPD = pd.concat([articlesPD, articlePD])
#     export_csv = articlesPD.to_csv(r"" + ROOT_DIR + '/Outputs/app_name_papers_final.csv', index=None, header=True)
#
# all_paper_search()

def build_database_onlyname(df):
    app_documented = []
    for i in range(len(df)):
        app_documented.append(
            [df.iloc[i]["App Name"]])
    return app_documented

def search_all_paper():
    df = pd.read_csv(r"" + ROOT_DIR + '/Outputs/dataset_serious_games.csv')
    serious_game_names = build_database_onlyname(df)
    articlesPD = pd.DataFrame.from_dict(serious_game_names)

    for name in serious_game_names:

        articleInfo = paper_search(name)
        articlePD = pd.DataFrame.from_dict(articleInfo)
        articlesPD = pd.concat([articlesPD, articlePD])

    export_csv = articlesPD.to_csv(r"" + ROOT_DIR + '/Outputs/app_name_papers_final.csv', index=None, header=True)


search_all_paper()



