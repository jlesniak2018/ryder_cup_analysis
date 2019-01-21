import abc, matplotlib, numpy as np
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import utils.Constants as Constants
import utils.MongoApi as MongoApi

from PlotPoint import PlotPoint
from scipy import stats

class StatMatchAggregator(object):
    def __init__(self):
        self.mongo_client = MongoApi.MongoClient()

    def get_results_by_stat_match_type_and_team(self):
        return self.get_results_by_stat_and_match_type(True)

    def get_results_by_stat_and_match_type(self, separate_by_team=False):
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

        stat_match_data = StatMatchData(separate_by_team=separate_by_team)
        for stat in Constants.PLAYER_STATS_URL_VALUE.keys():
            stat_match_data.data[stat] = self.__parse_matches(stat, separate_by_team)

        return stat_match_data

    def __parse_matches(self, stat, separate_by_team):
        matches_data = {}
        for match_type in Constants.MATCH_TYPES:
            cur_matches = self.mongo_client.find_matches_entry({"match_type": match_type})
            point_map = self.__parse_matches_entry(stat, match_type, cur_matches)

            if not separate_by_team:
                matches_data[match_type] = []
                for team_name, points in point_map.iteritems():
                    matches_data[match_type] += points
            else:
                matches_data[match_type] = {}
                for team_name, points in point_map.iteritems():
                    matches_data[match_type][team_name] = points

        return matches_data

    def __parse_matches_entry(self, stat, match_type, cur_matches):
        usa_label = Constants.TEAM_NAMES[0]
        europe_label = Constants.TEAM_NAMES[1]
        point_map = {usa_label: [], europe_label: []}
        for year, year_matches in cur_matches["matches"].items():
            for match in year_matches:
                cur_point_map = None
                if match_type == Constants.MATCH_TYPES[2]:
                    cur_point_map = self.__parse_singles_match(stat, year, match)
                else:
                    cur_point_map = self.__parse_team_match(stat, match_type, year, match)
                
                for key in cur_point_map.keys():
                    point_map[key] += cur_point_map[key]

        return point_map

    def __parse_singles_match(self, stat, year, match):
        usa_player = self.mongo_client.find_player_entry({"_id": match[Constants.SINGLES_MATCH_DB_ENTRY_FIELDS[3]]})
        europe_player = self.mongo_client.find_player_entry({"_id": match[Constants.SINGLES_MATCH_DB_ENTRY_FIELDS[4]]})

        singles_label = Constants.MATCH_TYPES[2]
        result_label = Constants.SINGLES_MATCH_DB_ENTRY_FIELDS[-1]
        usa_label = Constants.TEAM_NAMES[0]
        europe_label = Constants.TEAM_NAMES[1]
        point_map = {usa_label: [], europe_label: []}

        if year in usa_player["stats"].keys():
            point_map[usa_label].append(PlotPoint(usa_player["stats"][year][stat], match[result_label]))
        if year in europe_player["stats"].keys():
            point_map[europe_label].append(PlotPoint(europe_player["stats"][year][stat], -match[result_label]))

        return point_map

    def __parse_team_match(self, stat, match_type, year, match):
        usa_player1 = self.mongo_client.find_player_entry({"_id": match[Constants.TEAM_MATCH_DB_ENTRY_FIELDS[6]]})
        usa_player2 = self.mongo_client.find_player_entry({"_id": match[Constants.TEAM_MATCH_DB_ENTRY_FIELDS[7]]})
        europe_player1 = self.mongo_client.find_player_entry({"_id": match[Constants.TEAM_MATCH_DB_ENTRY_FIELDS[8]]})
        europe_player2 = self.mongo_client.find_player_entry({"_id": match[Constants.TEAM_MATCH_DB_ENTRY_FIELDS[9]]})

        result_label = Constants.TEAM_MATCH_DB_ENTRY_FIELDS[-1]
        usa_label = Constants.TEAM_NAMES[0]
        europe_label = Constants.TEAM_NAMES[1]
        point_map = {usa_label: [], europe_label: []}

        if year in usa_player1["stats"].keys():
            point_map[usa_label].append(PlotPoint(usa_player1["stats"][year][stat], match[result_label]))
        if year in usa_player2["stats"].keys():
            point_map[usa_label].append(PlotPoint(usa_player2["stats"][year][stat], match[result_label]))
        if year in europe_player1["stats"].keys():
            point_map[europe_label].append(PlotPoint(europe_player1["stats"][year][stat], -match[result_label]))
        if year in europe_player2["stats"].keys():
            point_map[europe_label].append(PlotPoint(europe_player2["stats"][year][stat], -match[result_label]))

        return point_map

class StatMatchData(object):
    def __init__(self, data={}, separate_by_team=False):
        self.data = data
        self.separate_by_team = separate_by_team
        self.axes_data = None

    def get_all_axes(self):
        if self.axes_data is None:
            self.axes_data = {}
            for stat in self.data.keys():
                self.axes_data[stat] = {}
                for match_type in self.data[stat].keys():
                    self.axes_data[stat][match_type] = {}
                    if not self.separate_by_team:
                        self.axes_data[stat][match_type]["x-axis"], self.axes_data[stat][match_type]["y-axis"] = self.__get_axes_pair(self.data[stat][match_type])
                    else:
                        for team_name in self.data[stat][match_type].keys():
                            self.axes_data[stat][match_type][team_name] = {}
                            self.axes_data[stat][match_type][team_name]["x-axis"], self.axes_data[stat][match_type][team_name]["y-axis"] = self.__get_axes_pair(self.data[stat][match_type][team_name])
        return self.axes_data

    def __get_axes_pair(self, plot_point_arr):
        x_axis = np.zeros(len(plot_point_arr))
        y_axis = np.zeros(len(plot_point_arr))
        for idx, data_point in enumerate(plot_point_arr):
            x_axis[idx] = data_point.x_val
            y_axis[idx] = data_point.y_val
        return x_axis, y_axis

    def plot_data(self, show_after_each_match=True):
        if self.axes_data is None:
            self.get_all_axes()

        for stat in self.axes_data.keys():
            for match_type in self.axes_data[stat].keys():
                if not self.separate_by_team:
                    x_axis = self.axes_data[stat][match_type]["x-axis"]
                    y_axis = self.axes_data[stat][match_type]["y-axis"]
                    self.__plot_match(x_axis,
                                      y_axis,
                                      '{} vs {} results'.format(stat, match_type),
                                      stat,
                                      match_type,
                                      'bo')
                else:
                    for team_name in self.axes_data[stat][match_type].keys():
                        x_axis = self.axes_data[stat][match_type][team_name]["x-axis"]
                        y_axis = self.axes_data[stat][match_type][team_name]["y-axis"]
                        self.__plot_match(x_axis,
                                          y_axis,
                                          '{} vs {} results ({})'.format(stat, match_type, team_name),
                                          stat,
                                          match_type,
                                          'bo' if team_name == Constants.TEAM_NAMES[-1] else 'ro')
                if show_after_each_match:
                    plt.show()
        if not show_after_each_match:
            plt.show()

    def __plot_match(self, x_axis, y_axis, title, stat, match_type, plot_point_style):
        fig, ax = plt.subplots()
        ax.set_title(title)
        ax.set_xlabel(stat)
        ax.set_ylabel(match_type)
        ax.plot(x_axis, y_axis, plot_point_style)

class StatMatchAnalyzer:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, stat_match_data):
        self.stat_match_data = stat_match_data
        self.transformed_data = None

    @abc.abstractmethod
    def get_transformed_data(self):
        pass

class StatMatchLinRegAnalyzer(StatMatchAnalyzer):
    def __init__(self, stat_match_data):
        super(StatMatchLinRegAnalyzer, self).__init__(stat_match_data)

    def get_transformed_data(self):
        if self.transformed_data is None:
            self.__lin_reg_all_data()
        return self.transformed_data

    def __lin_reg_all_data(self):
        if self.transformed_data is None:
            self.transformed_data = {}
            raw_data = self.stat_match_data.get_all_axes()
            for stat in raw_data.keys():
                self.transformed_data[stat] = {}
                for match_type in raw_data[stat].keys():
                    if not self.stat_match_data.separate_by_team:
                        lin_reg_result = self.__lin_reg_axes_pair(raw_data[stat][match_type]["x-axis"],
                                                                   raw_data[stat][match_type]["y-axis"])
                        self.transformed_data[stat][match_type] = lin_reg_result
                    else:
                        self.transformed_data[stat][match_type] = {}
                        for team_name in raw_data[stat][match_type].keys():
                            lin_reg_result = self.__lin_reg_axes_pair(raw_data[stat][match_type][team_name]["x-axis"],
                                                                       raw_data[stat][match_type][team_name]["y-axis"])
                            self.transformed_data[stat][match_type][team_name] = lin_reg_result

    def __lin_reg_axes_pair(self, x_axis, y_axis):
        #slope, intercept, rvalue, pvalue, stderr = stats.linregress(x_axis, y_axis)
        return stats.linregress(x_axis, y_axis)
