import Constants

from AbstractHTMLPageFetcherJob import AbstractHTMLPageFetcherJob
from StringFormatter import StringFormatter

class StatsHTMLPageFetcherJob(AbstractHTMLPageFetcherJob):
    def __init__(self, template_url, template_filename, dst_dir, years, stats_url_values=Constants.PLAYER_STATS_URL_VALUE):
        super(StatsHTMLPageFetcherJob, self).__init__(template_url, template_filename, dst_dir, years)
        self.stats_url_values = stats_url_values

    def get_formatted_urls(self):
        formatted_urls = StringFormatter.get_recursively_formatted_string(self.template_url, self.stats_url_values.values())
        return StringFormatter.get_recursively_formatted_strings(formatted_urls, self.years)

    def get_formatted_filenames(self):
        formatted_filenames = StringFormatter.get_recursively_formatted_string(self.template_filename, self.stats_url_values.keys())
        return StringFormatter.get_recursively_formatted_strings(formatted_filenames, self.years)
