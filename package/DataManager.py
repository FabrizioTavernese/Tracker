from datetime import date

class DataManager:
    def __init__(self):
        super().__init__()
        self.records = []

    def add(self, hours):
        
        record = {
            "horas" : hours,
            "fecha" : date.today().strftime("%d/%m/%Y")
        }
        self.records.append(record)
        return record
    
    def edit(self):
        print("soon...")

    def delete_last(self):
        if self.records:
            return self.records.pop()
        else:
            return None
        
    def get_all(self):
        return self.records