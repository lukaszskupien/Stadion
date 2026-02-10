import pandas as pd
from bs4 import BeautifulSoup
import requests
url = "https://www.transfermarkt.com/bolivia/spielplan/verein/5233/plus/0?saison_id=2026"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/116.0.0.0 Safari/537.36"
}

for sezon in range(2000,2026):
    payload  = {'saison_id':f"{sezon}"}
    r = requests.get(url,params=payload,headers=headers)
    if r.status_code == 200:
        with open(f"data/season_{sezon}.html", "w", encoding="utf-8") as f:
            f.write(r.text)
        print(f"{sezon} OK")
    else:
        print(f"Error dla sezonu:{sezon}")



        