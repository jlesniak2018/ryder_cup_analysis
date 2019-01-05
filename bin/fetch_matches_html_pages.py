from utils.MatchesHTMLPageFetcherJob import MatchesHTMLPageFetcherJob

if __name__=="__main__":
    MatchesHTMLPageFetcherJob("http://en.wikipedia.org/wiki/{}_Ryder_Cup",
                       "{}_Ryder_Cup.html",
                       "../resources/matches-html-pages/",
                       [2010, 2012, 2014, 2016, 2018]).execute()
