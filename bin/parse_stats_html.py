from utils.StatsHTMLParser import StatsHTMLParser

if __name__=="__main__":
    StatsHTMLParser("../resources/stats-html-pages/").parse_files()
    #StatsHTMLParser("../resources/stats-html-pages/",
    #                ["scoring_average"]).parse_files()
