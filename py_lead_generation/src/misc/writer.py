import csv
import os.path


class CsvWriter:
    '''
    CSW Writer class to create and append data to a csv file with fieldnames
    '''
    
    def __init__(self, filename: str, fieldnames: list[str]) -> None:
        '''
        `filename: str` - file name or file path to create, e.g., `'leads.csv'`
        `filename: list[str]` - field names/headings, should match data dictionary keys, e.g., `['id', 'name', 'phone_number']`

        Creates a new file or skip if file with such name already exists
        '''

        self.filename = filename
        self.fieldnames = fieldnames

        if not os.path.exists(filename):
            self._init()

    def _init(self) -> None:
        '''
        Initializes csv file by writing a new one with fieldnames
        '''
        with open(self.filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()

    def append(self, data: list[dict]) -> None:
        '''
        `data: list[dict]` - data to write, keys of this dictionary should match fieldnames

        Appends incoming `data` to the csv file
        '''
        with open(self.filename, 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            for d in data:
                writer.writerow(d)
