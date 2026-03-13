from Preprocess import teams,matches
from scipy.stats import percentileofscore
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

stats=[]


for team_name,team in teams.items():
    home_run = team[ team["venue"] == "H"]
    away_run = team[ team["venue"] == "A" ]
    wins = team[ team["points"] == 3]
    home_wins = home_run[home_run["points"] == 3]
    away_wins = away_run[away_run["points"] == 3]

    points_per_match = sum(team["points"]) / len(team)
    away_points_per_match = sum(away_run["points"])/ len(away_run)
    home_points_per_match = sum (home_run["points"]) / len(home_run)

    percent_of_wins = len(wins)/len(team)
    home_percent_of_wins = len(home_wins) / len(home_run) 
    away_percent_of_wins = len(away_wins) / len(away_run)

    points_diff = home_points_per_match - away_points_per_match
    stats.append(
        {
            "team":team_name,
            "points_per_match":points_per_match,
            "home_points_per_match":home_points_per_match,
            "away_points_per_match":away_points_per_match,
            "percent_of_wins":percent_of_wins,
            "home_percent_of_wins":home_percent_of_wins,
            "away_percent_of_wins":away_percent_of_wins,
            "points_diff":points_diff
        }
    )

    counts_H = ( [len(home_run[home_run["points"] == 0]),
                len(home_run[home_run["points"] == 1]),
                len(home_run[home_run["points"] == 3]) ] )
    counts_A = ( [len(away_run[away_run["points"] == 0]),
                len(away_run[away_run["points"] == 1]),
                len(away_run[away_run["points"] == 3] )] )
    

    fig, ax = plt.subplots(1,2)
    fig.suptitle(f"{team_name.capitalize()} Results (Past 20 Years)",fontweight="bold")
    results = ["loss","draw","win"]
    bar_colors = ['tab:red', 'tab:orange', 'tab:green']
    ax[0].bar(results,counts_H,color = bar_colors)
    ax[0].set_title("Home Run")
    ax[0].set_ylabel("number")

    ax[1].bar(results,counts_A,color = bar_colors)
    ax[1].set_title("Away Run")
    ax[1].set_ylabel("number")
    plt.savefig(fname=f"data/plots/{team_name+"_barplot"}")


stats = pd.DataFrame(stats)
print(stats)
others = stats.loc[stats["team"] != "bolivia","points_diff"]
bolivia_diff = stats.loc[stats["team"] == "bolivia","points_diff"].iloc[0]
p_value = np.mean( others >= bolivia_diff )

plt.figure(figsize=(12,6))

sns.stripplot(
    data=matches[matches["venue"]=="H"],
    x="oppRating",
    y="team",
    hue="result",
    order=stats.sort_values("points_diff",ascending=False)["team"],
    dodge=True,
    palette={"win":"green","draw":"orange","loss":"red"}
)

plt.xlabel("Opponent Elo rating")
plt.ylabel("Team")
plt.title("Home match result vs opponent strength")

plt.legend(title="Result")
plt.savefig("data/plots/home_stripplot")

sns.stripplot(
    data=matches[matches["venue"]=="A"],
    x="oppRating",
    y="team",
    hue="result",
    order=stats.sort_values("points_diff",ascending=False)["team"],
    dodge=True,
    palette={"win":"green","draw":"orange","loss":"red"}
)

plt.xlabel("Opponent Elo rating")
plt.ylabel("Team")
plt.title("Away match result vs opponent strength")

plt.legend(title="Result")
plt.savefig("data/plots/away_stripplot")
plt.show()
