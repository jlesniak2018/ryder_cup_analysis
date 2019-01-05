from AbstractHTMLPageFetcherJob import AbstractHTMLPageFetcherJob
from StringFormatter import StringFormatter

class MatchesHTMLPageFetcherJob(AbstractHTMLPageFetcherJob):
    def __init__(self, template_url, template_filename, dst_dir, years):
        super(MatchesHTMLPageFetcherJob, self).__init__(template_url, template_filename, dst_dir, years)

    def get_formatted_urls(self):
        return StringFormatter.get_recursively_formatted_string(self.template_url, self.years)

    def get_formatted_filenames(self):
        return StringFormatter.get_recursively_formatted_string(self.template_filename, self.years)
