# Collection labels
PLAYER_STATS_LABELS = ["Player name: ",
                       "Year: ",
                       "Ryder Cup team: ",
                       "Driving distance: ",
                       "Driving accuracy: ",
                       "Birdies per round: ",
                       "Bogeys per round: ",
                       "Putts per round: ",
                       "Greens in regulation: ",
                       "Strokes gained driving: ",
                       "Strokes gained tee-to-green: ",
                       "Strokes gained putting: ",
                       "Par 3 scoring: ",
                       "Par 4 scoring: ",
                       "Par 5 scoring: ",
                       "Scoring Average: "]

MATCH_INFO_LABELS = ["Match type: ",
                     "Year: ",
                     "USA player 1: ",
                     "USA player 2: ",
                     "Europe player 1: ",
                     "Europe player 2: ",
                     "Result: "]

# entry labels
PLAYER_DB_ENTRY_FIELDS = ["name",
                          "year",
                          "ryder_cup_team",
                          "driving_distance",
                          "driving_accuracy",
                          "birdies_per_round",
                          "bogeys_per_round",
                          "gir",
                          "putts_per_round",
                          "sg_driving",
                          "sg_tee_to_green",
                          "sg_putting",
                          "par_3_scoring",
                          "par_4_scoring",
                          "par_5_scoring"]

TEAM_MATCH_DB_ENTRY_FIELDS = ["match_type",
                              "year",
                              "usa_player1_name",
                              "usa_player2_name",
                              "europe_player1_name",
                              "europe_player2_name",
                              "usa_player1_stats_id",
                              "usa_player2_stats_id",
                              "europe_player1_stats_id",
                              "europe_player2_stats_id",
                              "result"]

SINGLES_MATCH_DB_ENTRY_FIELDS = ["year",
                                 "use_player_name",
                                 "europe_player_name",
                                 "usa_player_stats_id",
                                 "europe_player_stats_id",
                                 "result"]

MONGO_COLLECTION_NAMES = ["players",
                          "matches"]
TEAM_NAMES = ["USA",
              "Europe"]

MATCH_TYPES = ["fourball",
               "foursome",
               "singles"]

# URL mappings
PLAYER_STATS_URL_VALUE = {
    "driving_distance": "101",
    "driving_accuracy": "102",
    "birdies_per_round": "156",
    "bogeys_per_round": "02419",
    "gir": "103",
    "putts_per_round": "119",
    "sg_driving": "02567",
    "sg_tee_to_green": "02674",
    "sg_putting": "02564",
    "par_3_scoring": "142",
    "par_4_scoring": "143",
    "par_5_scoring": "144",
    "scoring_average": "120"
}

# Ryder cup players
RYDER_CUP_PLAYERS = {
        "Brooks Koepka": {
            "team": TEAM_NAMES[0],
            "years": ["2018", "2016"]
        },
        "Dustin Johnson": {
            "team": TEAM_NAMES[0],
            "years": ["2018", "2016", "2012", "2010"]
        },
        "Justin Thomas": {
            "team": TEAM_NAMES[0],
            "years": ["2018"]
        },
        "Patrick Reed": {
            "team": TEAM_NAMES[0],
            "years": ["2018", "2016", "2014"]
        },
        "Bubba Watson": {
            "team": TEAM_NAMES[0],
            "years": ["2018", "2014", "2012", "2010"]
        },
        "Jordan Spieth": {
            "team": TEAM_NAMES[0],
            "years": ["2018", "2016", "2014"]
        },
        "Rickie Fowler": {
            "team": TEAM_NAMES[0],
            "years": ["2018", "2016", "2014", "2010"]
        },
        "Webb Simpson": {
            "team": TEAM_NAMES[0],
            "years": ["2018", "2014", "2012"]
        },
        "Bryson DeChambeau": {
            "team": TEAM_NAMES[0],
            "years": ["2018"]
        },
        "Phil Mickelson": {
            "team": TEAM_NAMES[0],
            "years": ["2018", "2016", "2014", "2012", "2010"]
        },
        "Tiger Woods": {
            "team": TEAM_NAMES[0],
            "years": ["2018", "2012", "2010"]
        },
        "Tony Finau": {
            "team": TEAM_NAMES[0],
            "years": ["2018"]
        },
        "Jimmy Walker": {
            "team": TEAM_NAMES[0],
            "years": ["2016", "2014"]
        },
        "Brandt Snedeker": {
            "team": TEAM_NAMES[0],
            "years": ["2016", "2012"]
        },
        "Zach Johnson": {
            "team": TEAM_NAMES[0],
            "years": ["2016", "2014", "2012", "2010"]
        },
        "J.B. Holmes": {
            "team": TEAM_NAMES[0],
            "years": ["2016"]
        },
        "Matt Kuchar": {
            "team": TEAM_NAMES[0],
            "years": ["2016", "2014", "2012", "2010"]
        },
        "Ryan Moore": {
            "team": TEAM_NAMES[0],
            "years": ["2016"]
        },
        "Jim Furyk": {
            "team": TEAM_NAMES[0],
            "years": ["2014", "2012", "2010"]
        },
        "Keegan Bradley": {
            "team": TEAM_NAMES[0],
            "years": ["2014", "2012"]
        },
        "Hunter Mahan": {
            "team": TEAM_NAMES[0],
            "years": ["2014", "2010"]
        },
        "Jason Dufner": {
            "team": TEAM_NAMES[0],
            "years": ["2012"]
        },
        "Steve Stricker": {
            "team": TEAM_NAMES[0],
            "years": ["2012", "2010"]
        },
        "Jeff Overton": {
            "team": TEAM_NAMES[0],
            "years": ["2010"]
        },
        "Stewart Cink": {
            "team": TEAM_NAMES[0],
            "years": ["2010"]
        },
        "Francesco Molinari": {
            "team": TEAM_NAMES[1],
            "years": ["2018", "2012", "2010"]
        },
        "Justin Rose": {
            "team": TEAM_NAMES[1],
            "years": ["2018", "2016", "2014", "2012"]
        },
        "Tyrrell Hatton": {
            "team": TEAM_NAMES[1],
            "years": ["2018"]
        },
        "Tommy Fleetwood": {
            "team": TEAM_NAMES[1],
            "years": ["2018"]
        },
        "John Rahm": {
            "team": TEAM_NAMES[1],
            "years": ["2018"]
        },
        "Rory McIlroy": {
            "team": TEAM_NAMES[1],
            "years": ["2018", "2016", "2014", "2012", "2010"]
        },
        "Alex Noren": {
            "team": TEAM_NAMES[1],
            "years": ["2018"]
        },
        "Thorbjorn Olesen": {
            "team": TEAM_NAMES[1],
            "years": ["2018"]
        },
        "Paul Casey": {
            "team": TEAM_NAMES[1],
            "years": ["2018"]
        },
        "Sergio Garcia": {
            "team": TEAM_NAMES[1],
            "years": ["2018", "2016", "2014", "2012"]
        },
        "Ian Poulter": {
            "team": TEAM_NAMES[1],
            "years": ["2018", "2014", "2012", "2010"]
        },
        "Henrik Stenson": {
            "team": TEAM_NAMES[1],
            "years": ["2018", "2016", "2014"]
        },
        "Danny Willett": {
            "team": TEAM_NAMES[1],
            "years": ["2016"]
        },
        "Chris Wood": {
            "team": TEAM_NAMES[1],
            "years": ["2016"]
        },
        "Rafael Cabrera-Bello": {
            "team": TEAM_NAMES[1],
            "years": ["2016"]
        },
        "Andy Sullivan": {
            "team": TEAM_NAMES[1],
            "years": ["2016"]
        },
        "Matthew Fitzpatrick": {
            "team": TEAM_NAMES[1],
            "years": ["2016"]
        },
        "Lee Westwood": {
            "team": TEAM_NAMES[1],
            "years": ["2016", "2014", "2012", "2010"]
        },
        "Martin Kaymer": {
            "team": TEAM_NAMES[1],
            "years": ["2016", "2014", "2012", "2010"]
        },
        "Thomas Pieters": {
            "team": TEAM_NAMES[1],
            "years": ["2016"]
        },
        "Victor Dubuisson": {
            "team": TEAM_NAMES[1],
            "years": ["2014"]
        },
        "Jamie Donaldson": {
            "team": TEAM_NAMES[1],
            "years": ["2014"]
        },
        "Thomas Bjorn": {
            "team": TEAM_NAMES[1],
            "years": ["2014"]
        },
        "Graeme McDowell": {
            "team": TEAM_NAMES[1],
            "years": ["2014", "2012", "2010"]
        },
        "Stephen Gallacher": {
            "team": TEAM_NAMES[1],
            "years": ["2014"]
        },
        "Paul Lawrie": {
            "team": TEAM_NAMES[1],
            "years": ["2012"]
        },
        "Luke Donald": {
            "team": TEAM_NAMES[1],
            "years": ["2012", "2010"]
        },
        "Peter Hanson": {
            "team": TEAM_NAMES[1],
            "years": ["2012", "2010"]
        },
        "Nicolas Colsaerts": {
            "team": TEAM_NAMES[1],
            "years": ["2012"]
        },
        "Ross Fisher": {
            "team": TEAM_NAMES[1],
            "years": ["2010"]
        },
        "Miguel Angel Jimenez": {
            "team": TEAM_NAMES[1],
            "years": ["2010"]
        },
        "Edoardo Molinari": {
            "team": TEAM_NAMES[1],
            "years": ["2010"]
        },
        "Padraig Harrington": {
            "team": TEAM_NAMES[1],
            "years": ["2010"]
        }
}
