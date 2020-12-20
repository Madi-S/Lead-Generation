import csv

from my_config import order
from logger_config import get_logger

logger = get_logger('buffer')


class Buffer:
    lower_limit = 10
    upper_limit = 201
    fn = list(order.keys())

    def __init__(self, filename: str = 'leads.csv', buffer_size: int = 15):
        if not filename.endswith('.csv'):
            raise ValueError(
                'Incorrect filename specified. Filename should end with `.csv`')
        if not buffer_size in range(self.lower_limit, self.upper_limit):
            raise ValueError(
                f'Expected value between {self.upper_limit} and {self.upper_limit}. However, got {buffer_size}')

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
            print(f'Got duplicate or empty dictionary {info}')