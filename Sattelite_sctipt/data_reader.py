import json

class DataReader:
    DESCRIPTION_FILENAME = 'data/description.json'
    NAMES_FILENAME = 'data/names.txt'

    @staticmethod
    def get_description(filename=DESCRIPTION_FILENAME):
        with open(filename, 'r') as f:
            data = json.load(f)
        return data

    @staticmethod
    def get_names(filename=NAMES_FILENAME):
        with open(filename, 'r') as f:
            data = f.read()
        return data.split()
