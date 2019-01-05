import abc, bs4, MongoApi, os, re, unidecode, warnings

class AbstractHTMLParser:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, html_files_path, stats_to_parse=[]):
        self.html_files_path = html_files_path
        if type(stats_to_parse) != list:
            self.stats_to_parse = []
        else:
            self.stats_to_parse = stats_to_parse
        self.mongo_client = MongoApi.MongoClient()
        warnings.filterwarnings("error")

    @abc.abstractmethod
    def parse_files(self):
        pass

    def get_file_names(self):
        try:
            files = os.listdir(self.html_files_path)
            if len(self.stats_to_parse) != 0:
                filtered_files = []
                for stat in self.stats_to_parse:
                    for f in files:
                        if stat in f:
                            filtered_files.append(f)
                files = filtered_files
            print "file names to parse: {}".format(str(files))
            return files
        except TypeError as e:
            print e
            return None

    def get_beautifulsoup_object(self, file_name):
        soup = None
        with open(self.html_files_path+file_name, "r") as cur_file:
            soup = bs4.BeautifulSoup(cur_file.read(), "html.parser")
            cur_file.close()
        return soup

    @staticmethod
    def get_last_name_first_initial(player_name):
        name_list = player_name.split(' ')
        while '(' in name_list[-1]:
            name_list = name_list[0:-1]
        return [AbstractHTMLParser.clean_string(name_list[-1]), AbstractHTMLParser.clean_string(name_list[0][0])]

    @staticmethod
    def clean_string(string):
        try:
            string = unidecode.unidecode(string)
        except RuntimeWarning as e:
            #print "String is not a unicode object. Ignoring decode"
            pass

        return re.sub('[^a-zA-Z]+', '', string.strip()).lower()
