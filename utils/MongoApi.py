import pymongo, Constants

class MongoClient():
    def __init__(self, domain="localhost", port=27017):
        self.mongo_client = pymongo.MongoClient(domain, port)
        db = self.mongo_client.ryder_cup
        self.players = db[Constants.MONGO_COLLECTION_NAMES[0]]
        self.matches = db[Constants.MONGO_COLLECTION_NAMES[1]]

    def get_all_player_entries(self):
        return self.players.find({})

    def get_all_matches_entries(self):
        return self.matches.find({})

    def find_player_entry(self, condition):
        return self.players.find_one(condition)

    def find_player_entries(self, condition):
        return self.players.find(condition)

    def find_matches_entry(self, condition):
        return self.matches.find_one(condition)

    def find_matches_entries(self, condition):
        return self.matches.find(condition)

    def insert_player(self, player_name, stats_entries):
        player_entry = self.find_player_entry({Constants.PLAYER_DB_ENTRY_FIELDS[0]: player_name})
        if player_entry is None:
            mongo_entry = {
                Constants.PLAYER_DB_ENTRY_FIELDS[0]: player_name,
                "stats": stats_entries,
                Constants.PLAYER_DB_ENTRY_FIELDS[2]: Constants.RYDER_CUP_PLAYERS[player_name]["team"]
            }
            return self.players.insert_one(mongo_entry)
        else:
            return self.update_player(player_entry, stats_entries)

    def update_player(self, player_entry, stats_entries):
        for year, stats in stats_entries.iteritems():
            if year not in player_entry["stats"].keys():
                player_entry["stats"][year] = {}
            for stat_label, stat_val in stats.iteritems():
                player_entry["stats"][year][stat_label] = stat_val
        return self.players.update_one({"name": player_entry["name"]}, {"$set": {"stats": player_entry["stats"]}})

    def convert_singles_year(self, matches):
        for i in xrange(len(matches)):
            usa_player_name = matches[i][Constants.SINGLES_MATCH_DB_ENTRY_FIELDS[1]]
            europe_player_name = matches[i][Constants.SINGLES_MATCH_DB_ENTRY_FIELDS[2]]

            usa_player_id = self.find_player_entry({"name": usa_player_name})["_id"]
            europe_player_id = self.find_player_entry({"name": europe_player_name})["_id"]

            matches[i][Constants.SINGLES_MATCH_DB_ENTRY_FIELDS[3]] = usa_player_id
            matches[i][Constants.SINGLES_MATCH_DB_ENTRY_FIELDS[4]] = europe_player_id

    def convert_team_year(self, matches):
        for i in xrange(len(matches)):
            usa_player_name_1 = matches[i][Constants.TEAM_MATCH_DB_ENTRY_FIELDS[2]]
            usa_player_name_2 = matches[i][Constants.TEAM_MATCH_DB_ENTRY_FIELDS[3]]
            europe_player_name_1 = matches[i][Constants.TEAM_MATCH_DB_ENTRY_FIELDS[4]]
            europe_player_name_2 = matches[i][Constants.TEAM_MATCH_DB_ENTRY_FIELDS[5]]

            usa_player_id_1 = self.find_player_entry({"name": usa_player_name_1})["_id"]
            usa_player_id_2 = self.find_player_entry({"name": usa_player_name_2})["_id"]
            europe_player_id_1 = self.find_player_entry({"name": europe_player_name_1})["_id"]
            europe_player_id_2 = self.find_player_entry({"name": europe_player_name_2})["_id"]

            matches[i][Constants.TEAM_MATCH_DB_ENTRY_FIELDS[6]] = usa_player_id_1
            matches[i][Constants.TEAM_MATCH_DB_ENTRY_FIELDS[7]] = usa_player_id_2
            matches[i][Constants.TEAM_MATCH_DB_ENTRY_FIELDS[8]] = europe_player_id_1
            matches[i][Constants.TEAM_MATCH_DB_ENTRY_FIELDS[9]] = europe_player_id_2

    def insert_matches(self, matches, match_type):
        for year, matches_list in matches.items():
            if match_type == Constants.MATCH_TYPES[2]:
                self.convert_singles_year(matches_list)
            else:
                self.convert_team_year(matches_list)

        mongo_entry = {
            "match_type": match_type,
            "matches": matches
        }
        self.matches.insert_one(mongo_entry)
