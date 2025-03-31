import csv
from pathlib import Path
from ..models.operator import Operator

class OperatorRepository:
    def __init__(self):
        self.data = []
        self.load_data()
    
    def load_data(self):
        csv_path = Path(__file__).parent.parent.parent.parent / "resources" / "operadoras.csv"
        with open(csv_path, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                self.data.append(Operator(**row))
    
    def get_all_operators(self):
        return self.data