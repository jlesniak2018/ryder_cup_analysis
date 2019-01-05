import os, urllib2

class HTMLPageFetcher(object):
    def __init__(self, page_fetcher_job):
        self.page_fetcher_job = page_fetcher_job

    def fetch_and_save_html_pages(self):
        filepaths = self.get_filepaths()
        urls = self.page_fetcher_job.get_urls()
        for i in xrange(len(urls)):
            self.fetch_and_save_html_page(urls[i], filepaths[i])

    def get_filepaths(self):
        dst_dir = self.page_fetcher_job.get_dst_dir()
        filenames = self.page_fetcher_job.get_filenames()
        return map(lambda filename: os.path.join(dst_dir, filename), filenames)

    def fetch_and_save_html_page(self, url, filepath):
        html = self.fetch_html(url)
        self.save_html_as_file(html, filepath)

    def fetch_html(self, url):
        print "Fetching HTML for {}".format(url)
        response = urllib2.urlopen(url)
        return response.read()

    def save_html_as_file(self, html, filepath):
        print "Saving HTML in {}".format(filepath)
        with open(filepath, "w") as html_file:
            html_file.write(html)
            html_file.close()
