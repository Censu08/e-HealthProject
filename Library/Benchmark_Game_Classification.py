import pandas as pd


def run_benchmark_first_part():
    # We take the final dataset of serious games found with our algorithm and we extract the column "App Id"
    df_sg = pd.read_csv(r'../Outputs/dataset_seriousgames.csv', sep=",")
    ID_sg = df_sg["App Id"]
    # We take the benchmark dataset and we extract the fake games, the random apps and the serious games
    df_bm = pd.read_csv(r'../Sources/benchmark_data.csv', sep=";")
    fake_games = df_bm["FAKE GAMES"]
    random_apps = df_bm["RANDOM APPS"]
    serious_games = df_bm["SERIOUS GAMES"]
    # Important values
    seriousGamesInDataset = 0
    seriousGamesNotInDataset = 0
    randomAppsInDataset = 0
    randomAppsNotInDataset = 0
    fakeGamesInDataset = 0
    fakeGamesNotInDataset = 0
    for i in range(len(serious_games) - 1):
        flag = False
        for j in range(len(ID_sg)):
            if serious_games[i] == ID_sg[j]:
                seriousGamesInDataset += 1
                flag = True
                break
        if flag == False:
            seriousGamesNotInDataset += 1
    for i in range(len(random_apps) - 1):
        flag = False
        for j in range(len(ID_sg)):
            if random_apps[i] == ID_sg[j]:
                randomAppsInDataset += 1
                flag = True
                break
        if flag == False:
            randomAppsNotInDataset += 1
    for i in range(len(fake_games) - 1):
        flag = False
        for j in range(len(ID_sg)):
            if fake_games[i] == ID_sg[j]:
                fakeGamesInDataset += 1
                flag = True
                break
        if flag == False:
            fakeGamesNotInDataset += 1
    # sensitivity = TP / (TP + FN)
    # specificity = TN / (TN + FP)
    # Formulas to evaluate the performance
    accuracy = (seriousGamesInDataset + fakeGamesNotInDataset + randomAppsNotInDataset) / \
               (seriousGamesInDataset + seriousGamesNotInDataset +
                fakeGamesInDataset + fakeGamesNotInDataset +
                randomAppsInDataset + randomAppsNotInDataset)
    effective_accuracy = ((seriousGamesInDataset + fakeGamesNotInDataset + randomAppsNotInDataset) - (
                seriousGamesNotInDataset + fakeGamesInDataset + randomAppsInDataset)) / \
                         (seriousGamesInDataset + seriousGamesNotInDataset +
                          fakeGamesInDataset + fakeGamesNotInDataset +
                          randomAppsInDataset + randomAppsNotInDataset)
    sensitivity = seriousGamesInDataset / \
                  (seriousGamesInDataset + seriousGamesNotInDataset)
    specificity = (fakeGamesNotInDataset + randomAppsNotInDataset) / \
                  (fakeGamesNotInDataset + randomAppsNotInDataset + fakeGamesInDataset + randomAppsInDataset)
    # Results
    print("Accuracy: ", round(accuracy * 100, 1), "%")
    print("Relative Accuracy: ", round(effective_accuracy * 100, 1), "%")
    print("Sensitivity: ", round(sensitivity * 100, 1), "%")
    print("Specificity: ", round(specificity * 100, 1), "%")
