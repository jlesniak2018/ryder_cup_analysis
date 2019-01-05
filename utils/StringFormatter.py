class StringFormatter(object):
    @staticmethod
    def get_recursively_formatted_strings(strings_to_format, string_values):
        formatted_strings = []
        for string_to_format in strings_to_format:
            formatted_strings += StringFormatter.get_recursively_formatted_string(string_to_format, string_values)
        return formatted_strings

    @staticmethod
    def get_recursively_formatted_string(string_to_format, string_values):
        formatted_strings = []
        for string_value in string_values:
            formatted_strings.append(StringFormatter.__get_partially_formatted_string(string_to_format, string_value))
        return formatted_strings

    @staticmethod
    def __get_partially_formatted_string(string_to_format, string_value):
        string_to_format_split = string_to_format.split("{}", 1)
        formatted_string = string_to_format
        if len(string_to_format_split) > 1:
            formatted_string = string_to_format_split[0] + str(string_value) + string_to_format_split[1]
        return formatted_string
