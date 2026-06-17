import pandas as pd
file_path = "Data_set\\support_tickets.csv"

class DataLoader:

    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)

    def load_data(self):
        return self.df