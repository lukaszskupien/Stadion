import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from pathlib import Path

pd.set_option('future.no_silent_downcasting', True)

teams = {
    "argentina": None,
    "bolivia": None,
    "brazil":None,
    "chile": None,
    "colombia":None,
    "ecuador": None,
    "paraguay": None,
    "peru":None,
    "uruguay": None,
    "venezuela": None
}

eloRanking = pd.read_csv("data/elo/eloratings.csv")
eloRanking = eloRanking.tail(n=-46)
eloRanking["date"] = pd.to_datetime(eloRanking["date"])

for team in teams.keys():
    seasons = list(Path(f'data/teams/{team}').glob("*"))
    rows = []

    for season in seasons:
        with open(season) as fp:
            soup = BeautifulSoup(fp,features="lxml")
        boxes = soup.find_all("div",class_="box")
        
        for box in boxes:
            if "World Cup qualification South America" not in box.find("h2").text:
                continue
            table = box.find("div", class_= "responsive-table").find("table")

        contents = table.find("tbody").find_all("tr")

        for content in contents:
            cols = content.find_all("td")
            points = 1 

            result=cols[9].find("span")
            if "redtext" in result.attrs.get("class"): points=0
            elif "greentext" in result.attrs.get("class"): points=3
            
            goalDiff = result.text
            goalDiff = int(goalDiff.split(":")[0]) - int( goalDiff.split(":")[1].split(" ")[0] )
            if points == 0: goalDiff=-goalDiff

            rows.append({
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
    data = data.infer_objects(copy=False)

    data["date"] = pd.to_datetime(data["date"],dayfirst=True)
    data["time"] = pd.to_datetime(data["time"], format="%I:%M %p").dt.time
    data = data.sort_values(by="date")

    team_rating = eloRanking[ eloRanking["team"] == f"{team}".capitalize() ]

    #join żeby pobrać elo przeciwnika najbliższe datowo
    data = pd.merge_asof(
        data.sort_values("date"),
        eloRanking.sort_values("date")[["date","team","rating"]],
        left_on="date",
        right_on="date",
        direction="backward",
        left_by="opponent",
        right_by="team",
    )
    #join żeby pobrać elo teamu najbliższe datowo
    data = pd.merge_asof(
    data.sort_values("date"),
        team_rating.sort_values("date")[["date","team","rating"]],
        left_on="date",
        right_on="date",
        direction="backward",
        suffixes=["","rank"]
    )
    
    data["ranking"] = data["ratingrank"]
    data = data.drop(["team","teamrank","ratingrank"],axis=1) #dropping redundant columns
    
    data.rename(columns={"ranking":f"{team}_rating","rating":"oppRating"},inplace=True)
    teams[f"{team}"] = data
    matches = pd.concat(teams, names=["team"]).reset_index(level=0)
    matches["result"] = matches["points"].map({
    3: "win",
    1: "draw",
    0: "loss"
})








