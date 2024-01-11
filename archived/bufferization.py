import csv

from logger_config import get_logger


logger = get_logger('buffer')


class Buffer:
    lower_limit = 5
    upper_limit = 200
    fn = ['Title', 'Address', 'WebSite', 'PhoneNumber']

    def __init__(self, filename: str = 'leads.csv', buffer_size: int = 5):
        if not filename.endswith('.csv'):
            raise ValueError(
                'Incorrect filename specified. Filename should end with `.csv`')
        if not buffer_size in range(self.lower_limit, self.upper_limit + 1):
            raise ValueError(
                f'Expected value between {self.lower_limit} and {self.upper_limit}. However, got {buffer_size}')

        self._buffer_size = buffer_size
        self._filename = filename
        self._data = []

        with open(self._filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fn)
            writer.writeheader()

    def dump(self):
        with open('leads.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fn)
            for d in self._data:
                writer.writerow(d)
        self._data.clear()

    def store(self, info: dict):
        if info.get('Title') and not info in self._data:
            self._data.append(info)
            if len(self._data) >= self._buffer_size:
                self.dump()
        else:
            logger.warning('Got duplicate or empty dictionary %s', info)
