import csv

from config import order


class Buffer:
    lower_limit = 20
    upper_limit = 201
    fn = list(order.keys())

    def __init__(self, filename: str = 'leads.csv', buffer_size: int = 20):
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

    def _dump(self):
        with open('leads.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fn)
            for d in self._data:
                writer.writerow(d)
        

    def __iadd__(self, other: dict):
        print('In here!')
        self._data.append(dict)
        if len(self._data) >= self._buffer_size:
            self._dump()
            self._data.clear()
