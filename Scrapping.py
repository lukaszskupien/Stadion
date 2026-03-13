from pathlib import Path
import requests

teams = {
    "argentina":3437,
    "bolivia":5233,
    "brazil":3439,
    "chile":3700,
    "colombia":3816,
    "ecuador":5750,
    "paraguay":3581,
    "peru":3584,
    "uruguay":3449,
    "venezuela":3504
}

for team,team_id in teams.items():

    Path(f"data/teams/{team}").mkdir(exist_ok=True,parents=True)

    url = f"https://www.transfermarkt.com/{team}/spielplan/verein/{team_id}/plus/0"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/116.0.0.0 Safari/537.36"
    }

    for season in range(2000,2026): 
        
        if season in [2002,2006,2010,2014,2018]: 
            continue

        payload  = {'saison_id':f"{season}",'verein':f"{team_id}"}
        try:
            r = requests.get(url,params=payload,headers=headers)
            if r.status_code == 200:
                with open(f"data/teams/{team}/season_{season}.html", "w", encoding="utf-8") as f:
                    f.write(r.text)
                print(f"{team}: {season}: OK")
            else:
                print(f"Error for:{team} {season}!!!")

        except Exception as e:
                    print(f"Connection error: {e}")

        