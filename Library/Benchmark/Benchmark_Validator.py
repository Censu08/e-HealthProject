import pandas as pd
import os

from Library.Recognizer import *


def run_validator_benchmark():
    df_benchmark_game_classification_data = pd.read_csv(r"" + ROOT_DIR + '/Sources/benchmark_validation.csv', sep=",")
    validated_games = df_benchmark_game_classification_data["medical_games"]
    not_validated_games = df_benchmark_game_classification_data["fake_medical_games"]

    TP = 0
    TN = 0
    FP = 0
    FN = 0

    #validated_games = list(filter(lambda x: (x != nan), validated_games))



    for validated_game in validated_games:
        validated_game_papers = (validated_game, pubmed_search(validated_game))
        mega_string = meta_paper_creator(validated_game_papers)
        app_validation_level = search_keyword(mega_string)
        validation = validate(app_validation_level)
        if validation:
            TP = TP + 1
        else:
            FN = FN + 1
    for not_validated_game in not_validated_games:
        not_validated_game_papers = (not_validated_game, pubmed_search(not_validated_game))
        mega_string = meta_paper_creator(not_validated_game_papers)
        app_validation_level = search_keyword(mega_string)
        validation = validate(app_validation_level)
        if validation:
            FP = FP + 1
        else:
            TN = TN + 1
    print("uee")



run_validator_benchmark()
