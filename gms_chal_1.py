import csv
import json
from io import StringIO
from typing import Dict, List

class Meta(type): 
    def __new__(mcs, name, bases, attrs): 
        return super().__new__(mcs, name, bases, attrs)

class CSVConverter(metaclass=Meta):
    def __init__(self, csv_string: str):
        self.csv_string = csv_string

    def parse_csv(self) -> List[Dict]:
        try:
            csv_io = StringIO(self.csv_string)
            csv_reader = csv.DictReader(csv_io)
            data = [row for row in csv_reader]
            return data
        except csv.Error as e:
            raise ValueError(f"Error parsing CSV: {e}")

    def export_json(self, data: List[Dict]) -> str:
        try:
            return json.dumps(data, indent=4)
        except TypeError as e:
            raise ValueError(f"Error exporting JSON: {e}")

    def convert(self) -> str:
        csv_data = self.parse_csv()
        json_string = self.export_json(csv_data)
        return json_string

# Example usage:
csv_string = """name,age,city
John,30,New York
Alice,25,London
Bob,35,Paris"""

converter = CSVConverter(csv_string)
json_output = converter.convert()
print(json_output)