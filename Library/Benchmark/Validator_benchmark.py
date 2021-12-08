def run_validator_benchmark():
    # We take the final dataset of serious games found on pubmed and VALIDATED BY ALGORITHM and we extract the column "App name"
    df_MG = pd.read_csv(r'Outputs/dataset_Validated_games_by_algorithm.csv', sep=",")
    name_MG = df_MG["App name"]
    # We take the benchmark dataset and we extract Medical Games and Fake Medical Games
    df_bm = pd.read_csv(r'Sources/BenchmarkValidator_data.csv', sep=";")
    fake_medical_games = df_bm["FAKE GAMES"]
    medical_games = df_bm["SERIOUS GAMES"]
    # Important values
    MedicalGamesValidated = 0 #Games that the algorithm has correctly validated 
    MedicalGamesNotValidated = 0 #Games that the algorithm has not validated
    FakeMedicalGamesValidated= 0 #Games that the algorithm has mistakenly validated
    FakeMedicalGamesNotValidated = 0 #Games that the algorithm has correctly not validated (games foun on pubmed but haven't reliability)
    for i in range(len(medical_games) - 1):
        flag = False
        for j in range(len(name_MG)):
            if medical_games[i] == name_MG[j]:
                MedicalGamesValidated += 1
                flag = True
                break
        if flag == False:
            MedicalGamesNotValidated += 1

    for i in range(len(fake_medical_games) - 1):
        flag = False
        for j in range(len(name_MG)):
            if fake_medical_games[i] == name_MG[j]:
                FakeMedicalGamesValidated += 1
                flag = True
                break
        if flag == False:
            FakeMedicalGamesNotValidated += 1
    # sensitivity = TP / (TP + FN)
    # specificity = TN / (TN + FP)
    # Formulas to evaluate the performance
    accuracy = (MedicalGamesValidated + FakeMedicalGamesNotValidated ) / \
               (MedicalGamesValidated+ MedicalGamesNotValidated +
                FakeMedicalGamesValidated + FakeMedicalGamesNotValidated)
   
    sensitivity = MedicalGamesValidated / \
                  (MedicalGamesValidated + MedicalGamesNotValidated)
    specificity = FakeMedicalGamesNotValidated / \
                  (FakeMedicalGamesNotValidated + FakeMedicalGamesValidated)
    # Results
    print("Accuracy: ", round(accuracy * 100, 1), "%")
    print("Sensitivity: ", round(sensitivity * 100, 1), "%")
    print("Specificity: ", round(specificity * 100, 1), "%")
