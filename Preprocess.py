import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from pathlib import Path




eloRanking = pd.read_csv("data/elo/eloratings.csv")
eloRanking = eloRanking.tail(n=-46)
eloRanking["date"] = pd.to_datetime(eloRanking["date"])
print(eloRanking)


seasons = list(Path('data/html').glob("*"))
rows = []

for season in seasons:
    with open(season) as fp:
        soup = BeautifulSoup(fp,features="lxml")

    table = soup.find_all("div", class_= "responsive-table")[-1].find("table")
    contents = table.find("tbody").find_all("tr")


    
    for content in contents:
        cols = content.find_all("td")
        points = 1 

        result=cols[9].find("span")
        if "redtext" in result.attrs.get("class"): points=0
        elif "greentext" in result.attrs.get("class"): points=3
        
        goalDiff = result.text
        goalDiff = int(goalDiff.split(":")[0]) - int(goalDiff.split(":")[1])
        if points == 0: goalDiff=-goalDiff

        

        rows.append({
                "matchday": cols[0].text.strip(),
                "date": cols[1].text.strip(),
                "time": cols[2].text.strip(),
                "venue": cols[3].text.strip(),
                "ranking": cols[4].text.strip(),
                "opponent": cols[6].find("a").text.strip(),
                "system": cols[7].text.strip(),
                "attendance": cols[8].text.strip(),
                "result": cols[9].text.strip(),
                "points": points,
                "goalDiff": goalDiff
            })
        

data = pd.DataFrame(rows)

missing = ["Unknown","?","","x"]
data = data.replace(missing,np.nan)

data["date"] = pd.to_datetime(data['date'],dayfirst=True)
data["time"] = pd.to_datetime(data["time"]).dt.time
data = data.sort_values(by="date")

home_run = data[ data["venue"] == "H"]
away_run = data[ data["venue"] == "A" ]
wins = data[ data["points"] == 3]
home_wins = home_run[home_run["points"] == 3]
away_wins = away_run[away_run["points"] == 3]


points_per_match = sum(data["points"]) / len(data)
away_points_per_match = sum(away_run["points"])/ len(away_run)
home_points_per_match = sum (home_run["points"]) / len(home_run)

percent_of_wins = len(wins)/len(data)
home_percent_of_wins = len(home_wins) / len(home_run) 
away_percent_of_wins = len(away_wins) / len(away_run)

bolivia_ratings = eloRanking[eloRanking["team"] == "Bolivia"]

data = pd.merge_asof(
    data.sort_values("date"),
    eloRanking.sort_values("date")[["date","team","rating"]],
    left_on="date",
    right_on="date",
    direction="backward",
    left_by="opponent",
    right_by="team",
)
data = pd.merge_asof(
data.sort_values("date"),
    bolivia_ratings.sort_values("date")[["date","team","rating"]],
    left_on="date",
    right_on="date",
    direction="backward",
    suffixes=["","rank"]
)
data["ranking"] = data["ratingrank"]
data = data.drop(["team","teamrank","ratingrank"],axis=1)
data.rename(columns={"ranking":"rating","rating":"oppRating"},inplace=True)
print(data)


print(f"all: Points per match: {points_per_match} percent of wins:{away_percent_of_wins}\nhome: Points per match    {home_points_per_match} percent of wins:{home_percent_of_wins}\naway: Points per match: {away_points_per_match} percent of wins {away_percent_of_wins}")






