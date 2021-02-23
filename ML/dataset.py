import csv
import datetime
from functools import reduce
import os 


class Dataset:
    def __init__(self, file_path):
        self.raw_results = []
        self.processed_results = []

        with open(file_path) as stream:
            reader = csv.DictReader(stream)

            for row in reader:
                row['Date'] = datetime.datetime.strptime(row['Date'], "%d/%m/%Y")
                self.raw_results.append(row)

        self.processed_results = self.get_odd_stat(self.raw_results)
        print(self.processed_results)

    def get_odd_stat(self, raw_result):
        result = []
        for raw in self.raw_results:
            if raw['B365H']:
                processed_result = {
                        'result': raw['FTR'],
                        'odds-home': float(raw['B365H']),
                        'odds-draw': float(raw['B365D']),
                        'odds-away': float(raw['B365A']),
                }
                result.append(processed_result)

        return result

Dataset('ML/data/Ligue1.csv')