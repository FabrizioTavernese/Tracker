from datetime import date
from PySide6.QtCore import Qt

class DataManager:
    '''
    Manages the data (storage, retrieval, modification)
    '''
    def __init__(self):
        super().__init__()
        self.records = []

    def add(self, hours):
        record = {
            "hours" : hours,
            "date" : date.today().strftime("%d/%m/%Y")
        }
        self.records.append(record)
        return record
    
    def delete_record(self, record):
        if record in self.records:
            self.records.remove(record)
    
    def edit(self):
        print("soon...")

    def get_all(self):
        return self.records
