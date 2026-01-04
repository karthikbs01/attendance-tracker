import os,json

def load_json(path,default):
    if not os.path.exists(path):
        return default
    with open(path, 'r') as f:
        try:
            data = json.load(f)
            return data
        except Exception as e:
            print("Error loading JSON from {}: {}".format(path, e))
            return default

def save_json(path,data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        try:
            json.dump(data, f, indent=4)
        except Exception as e:
            print("Error saving JSON to {}: {}".format(path, e))