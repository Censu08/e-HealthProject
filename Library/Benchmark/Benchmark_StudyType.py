# Libraries
import pandas as pd
from pymed import PubMed
from Library.Recognizer import ROOT_DIR


def paper_search(pmid):
    pubmed = PubMed(tool='name_of_the_database', email='simonecensuales1998@gmail.com')
    results = pubmed.query(pmid, max_results=1)
    article_list = []
    article_info = []

    for article in results:
        # Print the type of object we've found (can be either PubMedBookArticle or PubMedArticle).
        # We need to convert it to dictionary with available function
        article_dict = article.toDict()
        article_list.append(article_dict)

    if len(article_list) != 0:
        # Generate list of dict records which will hold all article details that could be fetch from PUBMED API
        for article in article_list:
            # Sometimes article['pubmed_id'] contains list separated with comma - take first pubmedId in that list -
            # thats article pubmedId
            pubmed_id = article['pubmed_id'].partition('\n')[0]
            # Append article info to dictionary
            try:
                article_info.append({u'pmid': pmid,
                                     u'pubmed_id': pubmed_id,
                                     u'title': article['title'],
                                     u'keywords': article['keywords'],
                                     u'journal': article['journal'],
                                     u'abstract': article['abstract'],
                                     u'conclusions': article['conclusions'],
                                     u'results': article['results']})
            except (Exception,):
                continue
    else:
        # Append article info to dictionary
        article_info.append({u'pmid': "",
                             u'pubmed_id': "",
                             u'title': "",
                             u'keywords': "",
                             u'journal': "",
                             u'abstract': "",
                             u'conclusions': "",
                             u'results': ""})
    df = pd.DataFrame(article_info)
    return df


def build_database_onlyname(df):
    paper_documented = []
    for i in range(len(df)):
        paper_documented.append(
            [df.iloc[i]["pmid"]])
    return paper_documented


def search_all_paper():
    df = pd.read_csv(r"" + ROOT_DIR + '/Sources/benchmark_studytype.csv', sep=";")
    papers_pmid = build_database_onlyname(df)
    articles_pd = pd.DataFrame()
    for PMID in papers_pmid:
        article_df = paper_search(PMID)
        if article_df.iloc[0]["pmid"] != "":
            articles_pd = pd.concat([articles_pd, article_df])
    articles_pd.to_csv(r"" + ROOT_DIR + '/Sources/benchmark_studytypefinal.csv', index=False, header=True)


# search_all_paper()

def meta_paper_creator(df):
    mega_string = ""
    str1 = str(df['title'])
    if str1 is None:
        str1 = ""
    str2 = str(df['abstract'])
    if str2 is None:
        str2 = ""
    str3 = ""
    for keyword in df['keywords']:
        if keyword is not None:
            str3 = str3 + str(keyword) + " "
    str4 = str(df['journal'])
    if str4 is None:
        str4 = ""
    str5 = str(df['conclusions'])
    if str5 is None:
        str5 = ""
    str6 = str(df['results'])
    if str6 is None:
        str6 = ""
    mega_string = mega_string + str1 + str2 + str3 + str4 + str5 + str6
    return mega_string


def search_keyword(mega_string):
    if len(mega_string) < 1:
        return 0
    points = []
    with open(ROOT_DIR + '/Sources/Studies/CaseControl.txt') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in mega_string:
                points.append(4)
                break
    with open(ROOT_DIR + '/Sources/Studies/CaseSeries.txt') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in mega_string:
                points.append(2)
                break
    with open(ROOT_DIR + '/Sources/Studies/CohortStudy.txt') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in mega_string:
                points.append(5)
                break
    with open(ROOT_DIR + '/Sources/Studies/MetaAnalysis.txt') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in mega_string:
                points.append(7)
                break
    with open(ROOT_DIR + '/Sources/Studies/ObservationalStudy.txt') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in mega_string:
                points.append(3)
                break
    with open(ROOT_DIR + '/Sources/Studies/Other.txt') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in mega_string:
                points.append(1)
                break
    with open(ROOT_DIR + '/Sources/Studies/RCT.txt') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in mega_string:
                points.append(6)
                break
    with open(ROOT_DIR + '/Sources/Studies/SystematicReview.txt') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line in mega_string:
                points.append(7)
                break
    return points


def benchmark_studytype():
    df = pd.read_csv(r"" + ROOT_DIR + '/Sources/benchmark_studytypefinal.csv', sep=",")
    df2 = pd.read_csv(r"" + ROOT_DIR + '/Sources/benchmark_studytype.csv', sep=";")
    CC = 0 #correctly classified
    INCDIFF=0 #incremental score's differences
    for i in range(len(df)):
        mega_string = meta_paper_creator(df.iloc[i, :])
        points = search_keyword(mega_string)
        score = max(points, key=points.count)
        score2= df2.iloc[i]["Score"]
        INCDIFF += abs(score-score2)
        if score == df2.iloc[i]["Score"]:
                 CC +=1
    accuracy = CC / len(df)
    MAE=((INCDIFF)/len(df))/7
    print("accuracy: ", round(accuracy * 100, 1), "%")
    print("MAE: ", round(MAE * 100, 1), "%")


benchmark_studytype()