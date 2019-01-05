import numpy as np, matplotlib.pyplot as plt
import utils.Constants as Constants

from utils.MongoApi import MongoApi
from analysis.PlotPoint import PlotPoint


def stats_to_results():
    mongo_client = MongoApi.MongoClient()
    data = {}

    # Iterate over match types
    for stat in PLAYER_STATS_URL_VALUE.keys():
        data[stat] = {}
        parse_matches(data, stat)

    #TODO: plot in multiple ways:
    #       1 graph per data[stat] entry
    #       1 graph per data[stat][match_type] entry

def parse_matches(data, stat):
    for match_type in Constants.matches_types:
        data[stat][match_type] = []
        cur_matches = mongo_client.find_matches_entry({"match_type": match_type})
        if match_type == Constants.matches_types[2]:
            # Handle singles matches
            parse_singles_matches(data, stat, match_type, cur_matches)
        else:
            # Handle team matches
            parse_team_matches(data, stat, match_type, cur_matches)

def parse_singles_matches(data, stat, match_type, cur_matches):
    for year, year_matches in cur_matches["matches"].items():
        for match in year_matches:
            usa_player = mc.find_player_entry({"_id": match[Constants.SINGLES_MATCH_DB_ENTRY_FIELDS[3]]})
            europe_player = mc.find_player_entry({"_id": match[Constants.SINGLES_MATCH_DB_ENTRY_FIELDS[4]]})

            if year in usa_player["stats"].keys():
                data[stat][match_type].append(PlotPoint(usa_player["stats"][year][stat], match["result"]))
            if year in europe_player["stats"].keys():
                data[stat][match_type].append(PlotPoint(europe_player["stats"][year][stat], -match["result"]))

def parse_team_matches(data, stat, match_type, cur_matches):
    #6, 7, 8, 9
    for year, year_matches in cur_matches["matches"].items():
        for match in year_matches:
            usa_player1 = mc.find_player_entry({"_id": match[Constants.TEAM_MATCH_DB_ENTRY_FIELDS[6]]})
            usa_player2 = mc.find_player_entry({"_id": match[Constants.TEAM_MATCH_DB_ENTRY_FIELDS[7]]})
            europe_player1 = mc.find_player_entry({"_id": match[Constants.TEAM_MATCH_DB_ENTRY_FIELDS[8]]})
            europe_player2 = mc.find_player_entry({"_id": match[Constants.TEAM_MATCH_DB_ENTRY_FIELDS[9]]})

            if year in usa_player1["stats"].keys():
                data[stat][match_type].append(PlotPoint(usa_player1["stats"][year][stat], match["result"]))
            if year in usa_player2["stats"].keys():
                data[stat][match_type].append(PlotPoint(usa_player2["stats"][year][stat], match["result"]))
            if year in europe_player1["stats"].keys():
                data[stat][match_type].append(PlotPoint(europe_player1["stats"][year][stat], match["result"]))
            if year in europe_player2["stats"].keys():
                data[stat][match_type].append(PlotPoint(europe_player2["stats"][year][stat], match["result"]))

def stats_to_results_by_year():
        plot_year(cur_year, year)
    plt.show()

def plot_year(year_info, year):
    plot_team(year_info["usa_stats"],
              year_info["usa_results"],
              'ro',
              year,
              "USA",
              "gir",
              "singles")

    plot_team(year_info["europe_stats"],
              year_info["europe_results"],
              'bo',
              year,
              "Europe",
              "gir",
              "singles")

def plot_team(x, y, graphic, year, team, stat_label, match_type_label):
    fig, ax = plt.subplots()
    ax.set_title("{} {} {} vs {} results".format(year, team, stat_label, match_type_label))
    ax.set_xlabel(stat_label)
    ax.set_ylabel(match_type_label)
    ax.plot(x, y, graphic)

if __name__=="__main__":
    stats_to_results_by_year()
