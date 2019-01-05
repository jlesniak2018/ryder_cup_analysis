import Constants

from AbstractHTMLParser import AbstractHTMLParser

class MatchesHTMLParser(AbstractHTMLParser):
    def __init__(self, html_files_path):
        super(MatchesHTMLParser, self).__init__(html_files_path)
        self.session_headers_first_word = ["Session", "Friday's", "Saturday's", "Sunday's"]

    def parse_files(self):
        self.initialize_clean_player_names()
        self.initialize_mongo_entries()
        for file_name in self.get_file_names():
            self.cur_year = file_name.split("_")[0]
            self.cur_soup = self.get_beautifulsoup_object(file_name)
            self.parse_matches_data()
        self.write_matches_entries_to_mongo()
        #self.write_to_file()

    def initialize_clean_player_names(self):
        # Because players with the same last name are differentiated by their first inital on Wikipedia
        self.clean_player_names = {}
        for player_name in Constants.RYDER_CUP_PLAYERS:
            last_name, first_initial = self.get_last_name_first_initial(player_name)
            if last_name not in self.clean_player_names.keys():
                self.clean_player_names[last_name] = {}
            self.clean_player_names[last_name][first_initial] = player_name

    def initialize_mongo_entries(self):
        self.player_matches_mongo_entries = {match_type: {} for match_type in Constants.MATCH_TYPES}

    def parse_matches_data(self):
        self.relevant_page_elements = list(self.cur_soup.find_all(['h2', 'h3', 'tbody']))
        i = 0
        while i < len(self.relevant_page_elements):
            if self.is_session_header(self.relevant_page_elements[i]):
                session_start_idx, session_end_idx = self.get_sessions_boundaries(i) #end idx is exclusive
                self.parse_session(self.relevant_page_elements[session_start_idx:session_end_idx])
                i = session_end_idx - 1
            i += 1

    def is_session_header(self, page_element):
        if page_element.name == 'h2':
            for child_element in page_element.children:
                if child_element.string and child_element.string.split(' ')[0] in self.session_headers_first_word:
                    return True
        return False

    def get_sessions_boundaries(self, session_header_idx):
        session_header_idx += 1
        session_start_idx = session_header_idx
        while self.relevant_page_elements[session_header_idx].name != 'h2':
            session_header_idx += 1
        session_end_idx = session_header_idx
        return (session_start_idx, session_end_idx)

    def parse_session(self, session_elements):
        i = 0
        while i < len(session_elements):
            if session_elements[i].name == 'h3' and i < len(session_elements) - 1:
                sessions_parsed = self.parse_h3_element(session_elements[i], session_elements[i+1])
                i += sessions_parsed
            elif session_elements[i].name == 'tbody':
                self.parse_match_results_table(Constants.MATCH_TYPES[-1], session_elements[i])
            i += 1

    def parse_h3_element(self, h3_element, potential_table_element):
        sessions_seen = 0
        children_list = list(h3_element.children)
        for child_element in children_list:
            if child_element.string:
                sessions_seen += 1
                match_type_string = self.get_match_type_string(child_element)
                if match_type_string in Constants.MATCH_TYPES and potential_table_element.name == 'tbody':
                    self.parse_match_results_table(match_type_string, potential_table_element)
        return sessions_seen

    def get_match_type_string(self, match_header_element):
        return self.clean_string(match_header_element.string.split(' ')[-1])[0:8]

    def parse_match_results_table(self, match_type_string, match_results_table):
        ResultsTable(match_type_string, match_results_table, self).get_parsed_results()

    def write_matches_entries_to_mongo(self):
        for match_type, year_map in self.player_matches_mongo_entries.items():
            self.mongo_client.insert_matches(year_map, match_type)

    def write_to_file(self):
        # Print to file for sanity check
        with open("./parse_matches_results.txt", "w") as f:
            for match_type, year_map in self.player_matches_mongo_entries.items():
                f.write(match_type+":\n")
                for year, match_list in year_map.items():
                    f.write("\t"+year+":\n")
                    for match in match_list:
                        if len(match) == 3:
                            f.write("\t\t"+match[Constants.SINGLES_MATCH_DB_ENTRY_FIELDS[1]]+
                                    " played "+match[Constants.SINGLES_MATCH_DB_ENTRY_FIELDS[2]]+"\n")
                            f.write("\t\tThe score was "+str(match[Constants.SINGLES_MATCH_DB_ENTRY_FIELDS[5]])+"\n")
                        else:
                            f.write("\t\t"+match[Constants.TEAM_MATCH_DB_ENTRY_FIELDS[2]]+" and "+
                                    match[Constants.TEAM_MATCH_DB_ENTRY_FIELDS[3]]+" played "+
                                    match[Constants.TEAM_MATCH_DB_ENTRY_FIELDS[4]]+" and "+
                                    match[Constants.TEAM_MATCH_DB_ENTRY_FIELDS[5]]+"\n")
                            f.write("\t\tThe score was "+str(match[Constants.TEAM_MATCH_DB_ENTRY_FIELDS[10]])+"\n")
                        f.write("\n")
                f.write("\n")
            f.close()


#TODO: communicate with MatchesHTMLParser object the data from each parsed row (left players, right players, score)
class ResultsTable(object):
    def __init__(self, match_type_string, match_results_table, parent_parser):
        self.match_type_string = match_type_string
        self.match_results_table = match_results_table
        self.parent_parser = parent_parser

    def get_parsed_results(self):
        self.table_row_elements = list(self.match_results_table.find_all('tr'))
        self.left_team, self.right_team = self.get_teams_from_header_row(self.table_row_elements[0])
        self.parse_results_rows()

    def get_teams_from_header_row(self, header_row):
        th_children = list(header_row.find_all('th'))
        left_team = self.get_team(th_children[0])
        right_team = self.get_team(th_children[2])
        return (left_team, right_team)

    def get_team(self, team_cell):
        a_child = team_cell.find('a')
        if AbstractHTMLParser.clean_string(a_child['title']) == AbstractHTMLParser.clean_string(Constants.TEAM_NAMES[1]):
            return Constants.TEAM_NAMES[1]
        return Constants.TEAM_NAMES[0]

    def parse_results_rows(self):
        for i in xrange(1, len(self.table_row_elements)):
            cur_row = self.table_row_elements[i]
            td_children = list(cur_row.find_all('td'))
            if self.is_match_row(td_children):
                self.parse_results_row(td_children)

    def is_match_row(self, row_cells):
        if len(row_cells) > 0:
            a_child = row_cells[0].find('a')
            return a_child and a_child['title']
        return False

    def parse_results_row(self, row_cells):
        for cell_idx in xrange(3): # row has three relevent cells: left team | score | right team
            a_children = row_cells[cell_idx].find_all('a')
            if cell_idx == 0: # left team cell
                self.left_team_players = self.get_players_from_cell(a_children)
            elif cell_idx == 2: # right team cell
                self.right_team_players = self.get_players_from_cell(a_children)
            else: # score cell
                self.score = self.get_formatted_score(row_cells[cell_idx].text, a_children)
        self.add_mongo_entry()

    def get_players_from_cell(self, cell_elements):
        players = []
        for player_idx in xrange(len(cell_elements)):
            last_name, first_initial = AbstractHTMLParser.get_last_name_first_initial(cell_elements[player_idx]['title'])
            players.append(self.parent_parser.clean_player_names[last_name][first_initial])
        return players

    def get_formatted_score(self, score_string, cell_elements):
        score = 0
        if AbstractHTMLParser.clean_string(score_string) != 'halved':
            score = int(score_string.strip().split(' ')[0])
            if AbstractHTMLParser.clean_string(cell_elements[0]['title'][0]) == AbstractHTMLParser.clean_string(Constants.TEAM_NAMES[1][0]): # Title is sometimes Europe, sometimes European Union
                score *= -1 # European wins are negative values, American wins are positive values
        return score

    def add_mongo_entry(self):
        if self.parent_parser.cur_year not in self.parent_parser.player_matches_mongo_entries[self.match_type_string].keys():
            self.parent_parser.player_matches_mongo_entries[self.match_type_string][self.parent_parser.cur_year] = []
        is_usa_left = self.left_team == Constants.TEAM_NAMES[0]
        if self.is_singles_table():
            self.parent_parser.player_matches_mongo_entries[self.match_type_string][self.parent_parser.cur_year].append({
                Constants.SINGLES_MATCH_DB_ENTRY_FIELDS[1]: self.left_team_players[0] if is_usa_left else self.right_team_players[0],
                Constants.SINGLES_MATCH_DB_ENTRY_FIELDS[2]: self.right_team_players[0] if is_usa_left else self.left_team_players[0],
                Constants.SINGLES_MATCH_DB_ENTRY_FIELDS[5]: self.score
            })
        else:
            self.parent_parser.player_matches_mongo_entries[self.match_type_string][self.parent_parser.cur_year].append({
                Constants.TEAM_MATCH_DB_ENTRY_FIELDS[2]: self.left_team_players[0] if is_usa_left else self.right_team_players[0],
                Constants.TEAM_MATCH_DB_ENTRY_FIELDS[3]: self.left_team_players[1] if is_usa_left else self.right_team_players[1],
                Constants.TEAM_MATCH_DB_ENTRY_FIELDS[4]: self.right_team_players[0] if is_usa_left else self.left_team_players[0],
                Constants.TEAM_MATCH_DB_ENTRY_FIELDS[5]: self.right_team_players[1] if is_usa_left else self.left_team_players[1],
                Constants.TEAM_MATCH_DB_ENTRY_FIELDS[10]: self.score
            })

    def is_singles_table(self):
        return self.match_type_string == Constants.MATCH_TYPES[-1]
