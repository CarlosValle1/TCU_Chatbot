import json

class DataPersistenceManager:
    data_path = './data/'
    data_access_file_name = data_path + "data_access.json"

    def get_requested_filename(self, simple_filename: str):
        answer = ''
        with open(self.data_access_file_name, 'r') as file:
            file_as_json = json.load(file)
            names_map = file_as_json[0]
            for name in names_map:
                if name == simple_filename:
                    answer = self.data_path + names_map[name]
                    break
        return answer

    def get_data(self, simple_filename: str):
        filename = self.get_requested_filename(simple_filename)
        data_map = ''
        with open(filename, 'r') as file:
            file_as_json = json.load(file)
            data_map = file_as_json[1]['entries']
        return data_map
