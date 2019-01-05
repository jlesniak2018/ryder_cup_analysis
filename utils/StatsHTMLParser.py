import Constants

from AbstractHTMLParser import AbstractHTMLParser

class StatsHTMLParser(AbstractHTMLParser):
    def __init__(self, html_files_path, stats_to_parse=[]):
        super(StatsHTMLParser, self).__init__(html_files_path, stats_to_parse)

    def parse_files(self):
        self.initialize_clean_player_names()
        self.initialize_mongo_entries()
        for file_name in self.get_file_names():
            stat, year = file_name.split(".")[0].rsplit("_", 1)
            soup = self.get_beautifulsoup_object(file_name)
            self.parse_table_rows(soup, stat, year)
        self.write_player_entries_to_mongo()
        #self.write_to_file()

    def initialize_clean_player_names(self):
        self.clean_player_names = {self.clean_string(name): name for name in Constants.RYDER_CUP_PLAYERS}

    def initialize_mongo_entries(self):
        self.player_stats_mongo_entries = {player_name: {"stats": {}} for player_name in self.clean_player_names.values()}

    def parse_table_rows(self, soup, stat, year):
        table_rows = list(soup.find_all("tr"))
        for i in xrange(2, len(table_rows)):
            self.parse_table_row(table_rows[i], stat, year)

    def parse_table_row(self, table_row, stat, year):
        table_row_children = list(table_row.children)
        player_name = table_row_children[5].find_all("a")[0].string.encode("utf-8")
        clean_player_name = self.clean_string(player_name)
        stat_val = float(table_row_children[8].string)
        self.add_player_stat(clean_player_name, stat_val, stat, year)

    def add_player_stat(self, player_name, stat_val, stat, year):
        if self.is_valid_entry(player_name, year):
            self.ensure_year_entry_exists(player_name, year)
            self.player_stats_mongo_entries[self.clean_player_names[player_name]]["stats"][year][stat] = stat_val

    def is_valid_entry(self, player_name, year):
        return player_name in self.clean_player_names and year in Constants.RYDER_CUP_PLAYERS[self.clean_player_names[player_name]]["years"]

    def ensure_year_entry_exists(self, player_name, year):
        if year not in self.player_stats_mongo_entries[self.clean_player_names[player_name]]["stats"].keys():
            self.player_stats_mongo_entries[self.clean_player_names[player_name]]["stats"][year] = {}

    def write_player_entries_to_mongo(self):
        for player_name, player_stats in self.player_stats_mongo_entries.items():
            self.mongo_client.insert_player(player_name, player_stats["stats"])

    def write_to_file(self):
        with open("./parse_results.txt", "w") as f:
            for player_name, player_stats in self.player_stats_mongo_entries.items():
                self.write_player_to_file(player_name, player_stats, f)
            f.close()

    def write_player_to_file(self, player_name, player_stats, f):
        f.write(player_name+":\n")
        for year, stat_list in player_stats["stats"].items():
            self.write_stats_to_file(year, stat_list, f)
        f.write("\n")

    def write_stats_to_file(self, year, stat_list, f):
        f.write("\t"+year+":\n")
        for stat_key, stat_val in stat_list.items():
            f.write("\t\t"+stat_key+": "+str(stat_val)+"\n")
