import abc

from HTMLPageFetcher import HTMLPageFetcher

class AbstractHTMLPageFetcherJob:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, template_url=None, template_filename=None, dst_dir=None, years=None):
        self.template_url = template_url
        self.template_filename = template_filename
        self.dst_dir = dst_dir
        self.years = years

    @abc.abstractmethod
    def get_formatted_urls(self):
        pass

    @abc.abstractmethod
    def get_formatted_filenames(self):
        pass

    def execute(self):
        page_fetcher = HTMLPageFetcher(self)
        page_fetcher.fetch_and_save_html_pages()

    def get_urls(self):
        return self.get_formatted_urls()

    def get_filenames(self):
        return self.get_formatted_filenames()

    def get_dst_dir(self):
        return self.dst_dir
