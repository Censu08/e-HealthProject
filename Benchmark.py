import pandas as pd

# We take the final dataset of serious games found with our algorithm and we extract the column "App Id"
df_sg = pd.read_csv(r'C:\Users\Gilles FACCIN\Desktop\POLIMI 2021-2022\E-HEALTH METHODS\PROJECT\dataset_seriousgames.csv', sep = ",")
ID_sg = df_sg["App Id"]

# We take the benchmark dataset and we extract the fake games, the random apps and the serious games as lists
df_bm = pd.read_csv(r'C:\Users\Gilles FACCIN\Desktop\POLIMI 2021-2022\E-HEALTH METHODS\PROJECT\benchmark_data.csv', sep = ";")
fake_games = df_bm["FAKE GAMES"]
random_apps = df_bm["RANDOM APPS"]
serious_games = df_bm["SERIOUS GAMES"]

# Important values
TP = 0                 # True positives
FN = 0                 # False negatives
FP = 0                 # False positives
TN = 0                 # True negatives
nb_misleading = 0      # Number of misleading serious games detected as serious games
nb_undetected_ra = 0   # Number of random apps falsely detected as serious games

for i in range(len(serious_games)):
    if serious_games[i] in ID_sg:
        TP +=1
    else:
        FN += 1
for i in range(len(random_apps)):
    if random_apps[i] in ID_sg:
        FP += 1
        nb_undetected_ra += 1
    else:
        TN += 1
for i in range(len(fake_games)):
    if fake_games[i] in ID_sg:
        FP +=1
        nb_misleading += 1
    else:
        TN +=1

# Formulas to evaluate the performance
accuracy = (TP + TN)/(TP + TN + FP + FN)
relative_accuracy = (TP + nb_misleading - nb_undetected_ra)/(TP + TN + FP + FN)
sensitivity = TP/(TP + FN)
specificity = TN/(TN + FP)

# Results
print("Accuracy: ", accuracy)
print("Relative accuracy: ", relative_accuracy)
print("Sensitivity: ", sensitivity)
print("Specificity: ", specificity)