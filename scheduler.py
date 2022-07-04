# Import dependencies
from flask import Flask, render_template, request
import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import date
import json
import os
from sqlalchemy import create_engine

# Find environment variables
DATABASE_URL = os.environ.get("DATABASE_URL", None)


# Get all players' name, team name, position
urlString = "https://api.myfantasyleague.com/2022/export?TYPE=players"
response = requests.get(urlString)
soup = BeautifulSoup(response.content,'xml')
data = []
players = soup.find_all('player')
for i in range(len(players)):
    rows = [players[i].get("id"), players[i].get("name"), players[i].get("position"), players[i].get("team")]
    data.append(rows)
player_df = pd.DataFrame(data)
player_df.columns=['PlayerID','Name', 'Position', 'Team']

# Get Shark Ranks
urlString = "https://api.myfantasyleague.com/2022/export?TYPE=playerRanks"
response = requests.get(urlString)
soup = BeautifulSoup(response.content,'xml')
data = []
sharkRanks = soup.find_all('player')
for i in range(len(sharkRanks)):
    rows = [sharkRanks[i].get("id"), sharkRanks[i].get("rank")]
    data.append(rows)
shark_df = pd.DataFrame(data)
shark_df.columns=['PlayerID','SharkRank']
shark_df['SharkRank'] = shark_df['SharkRank'].astype('int32')

# Get adp
urlString = "https://api.myfantasyleague.com/2022/export?TYPE=adp"
response = requests.get(urlString)
soup = BeautifulSoup(response.content,'xml')
data = []
players = soup.find_all('player')
for i in range(len(players)):
    rows = [players[i].get("id"), players[i].get("averagePick")]
    data.append(rows)
adp_df = pd.DataFrame(data)
adp_df.columns=['PlayerID','ADP']
adp_df['ADP'] = adp_df['ADP'].astype('float32')

# Merge all dfs
complete = player_df.merge(shark_df, on='PlayerID', how='left').merge(adp_df, on='PlayerID', how='left')
complete['SharkRank'].fillna(3000, inplace=True)
complete['ADP'].fillna(3000, inplace=True)
complete = complete.sort_values(by=['SharkRank'])
complete.reset_index(inplace=True, drop=True)


# Save to database
engine = create_engine(DATABASE_URL, echo = False)
complete.to_sql("player_df", con = engine, if_exists='replace')

