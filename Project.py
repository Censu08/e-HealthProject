## Phase I: Identification of serious games for kids
import json
import play_scraper
from google_play_scraper import app
import pandas as pd

df = pd.read_csv(r'C:\Users\Gilles FACCIN\Desktop\Polimi 2021-2022\E-HEALTH METHODS\Practices\Google-Playstore.csv')
print(df)





df_edu = df[df["Category"] == "4 year old kids"]
#"Education","Educational","Family","Learn"]]
df_edu.head()



# print(json_result["age"])

# Extract information (title, description, learning category, ratings, expert validation, reviews, age range, games)

# Build a database of serious games

# Clean the database


## Phase IIa: Characterisation of relevant serious games

# Extract information from the PUBMED webpages

# Select relevant publications and create database out of them

# Characterise publications - identify relevant information from the texts