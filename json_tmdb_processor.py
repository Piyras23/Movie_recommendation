#print(2+2)
# For tmdb data: will use sunday for EDA  
import os
import json
import pandas as pd

class JSONProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.data_frame = pd.DataFrame()

    def process_json_files(self):
        files = os.listdir(self.folder_path)

        for file_name in files:
            file_path = os.path.join(self.folder_path, file_name)

            if file_name.endswith('.json'):
                json_data = self.load_json(file_path)
                self.process_data(json_data)

    def load_json(self, file_path):
        try:
            with open(file_path, 'r') as json_file:
                return json.load(json_file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {file_path}: {e}")
            return None
        
    def process_data(self, json_data):
        self.data_frame = self.data_frame.append(json_data, ignore_index=True)

    def get_data_frame(self):
        return self.data_frame
    
    