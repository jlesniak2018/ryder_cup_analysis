import numpy as np, matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import utils.Constants as Constants
import utils.MongoApi as MongoApi

from analysis.PlotPoint import PlotPoint

data = {}
mongo_client = MongoApi.MongoClient()

def stats_to_results():
    # structure of data dict:
    # {
    #     '<stat key>': {
    #         '<match type>': [
    #             Point(x_val:stat_val, y_val:match_result),
    #             Point(x_val:stat_val, y_val:match_result),
    #             ...
    #         ],
    #         ...
    #     },
    #     ...
    # }

    #TODO: plot in multiple ways:
    #       1 graph per data[stat][match_type] array
    #       1 graph per data[stat] entry

    for stat in Constants.PLAYER_STATS_URL_VALUE.keys():
        data[stat] = {}
        parse_matches(stat)

    #for stat in data.keys():
    #    print "STAT: {}".format(stat)
    #    for match_type in data[stat].keys():
    #        print "\tMATCH_TYPE: {}".format(match_type)
    #        for point in data[stat][match_type]:
    #            print "\t\t{}".format(point.str())

    for stat in data.keys():
        for match_type in data[stat].keys():
            plot_match(stat, match_type)
    plt.show()

def parse_matches(stat):
    for match_type in Constants.MATCH_TYPES:
        data[stat][match_type] = []
        cur_matches = mongo_client.find_matches_entry({"match_type": match_type})
        parse_matches_entry(stat, match_type, cur_matches)

def parse_matches_entry(stat, match_type, cur_matches):
    for year, year_matches in cur_matches["matches"].items():
        for match in year_matches:
            if match_type == Constants.MATCH_TYPES[2]:
                parse_singles_match(stat, year, match)
            else:
                parse_team_match(stat, match_type, year, match)

def parse_singles_match(stat, year, match):
    usa_player = mongo_client.find_player_entry({"_id": match[Constants.SINGLES_MATCH_DB_ENTRY_FIELDS[3]]})
    europe_player = mongo_client.find_player_entry({"_id": match[Constants.SINGLES_MATCH_DB_ENTRY_FIELDS[4]]})
    singles_label = Constants.MATCH_TYPES[2]
    result_label = Constants.SINGLES_MATCH_DB_ENTRY_FIELDS[-1]

    if year in usa_player["stats"].keys():
        data[stat][singles_label].append(PlotPoint(usa_player["stats"][year][stat], match[result_label]))
    if year in europe_player["stats"].keys():
        data[stat][singles_label].append(PlotPoint(europe_player["stats"][year][stat], -match[result_label]))

def parse_team_match(stat, match_type, year, match):
    usa_player1 = mongo_client.find_player_entry({"_id": match[Constants.TEAM_MATCH_DB_ENTRY_FIELDS[6]]})
    usa_player2 = mongo_client.find_player_entry({"_id": match[Constants.TEAM_MATCH_DB_ENTRY_FIELDS[7]]})
    europe_player1 = mongo_client.find_player_entry({"_id": match[Constants.TEAM_MATCH_DB_ENTRY_FIELDS[8]]})
    europe_player2 = mongo_client.find_player_entry({"_id": match[Constants.TEAM_MATCH_DB_ENTRY_FIELDS[9]]})
    result_label = Constants.TEAM_MATCH_DB_ENTRY_FIELDS[-1]

    if year in usa_player1["stats"].keys():
        data[stat][match_type].append(PlotPoint(usa_player1["stats"][year][stat], match[result_label]))
    if year in usa_player2["stats"].keys():
        data[stat][match_type].append(PlotPoint(usa_player2["stats"][year][stat], match[result_label]))
    if year in europe_player1["stats"].keys():
        data[stat][match_type].append(PlotPoint(europe_player1["stats"][year][stat], -match[result_label]))
    if year in europe_player2["stats"].keys():
        data[stat][match_type].append(PlotPoint(europe_player2["stats"][year][stat], -match[result_label]))

def plot_match(stat, match_type):
    data_arr = data[stat][match_type]
    x_axis = np.zeros(len(data_arr))
    y_axis = np.zeros(len(data_arr))

    for idx, data_point in enumerate(data_arr):
        x_axis[idx] = data_point.x_val
        y_axis[idx] = data_point.y_val
    
    fig, ax = plt.subplots()
    ax.set_title('{} vs {} results'.format(stat, match_type))
    ax.set_xlabel(stat)
    ax.set_ylabel(match_type)
    ax.plot(x_axis, y_axis, 'bo')

if __name__=="__main__":
    stats_to_results()
