from utils.StatsHTMLPageFetcherJob import StatsHTMLPageFetcherJob

if __name__=="__main__":
    # Fetch pages for all stats
    StatsHTMLPageFetcherJob("https://www.pgatour.com/stats/stat.{}.{}.html",
                            "{}_{}.html",
                            "../resources/stats-html-pages/",
                            [2010, 2012, 2014, 2016, 2018]).execute()
    # Fetch pages for custom set of stats
    #StatsHTMLPageFetcherJob("https://www.pgatour.com/stats/stat.{}.{}.html",
    #                        "{}_{}.html",
    #                        "../resources/stats-html-pages/",
    #                        [2010, 2012, 2014, 2016, 2018],
    #                        {
    #                            "scoring_average": "120"
    #                        }).execute()
