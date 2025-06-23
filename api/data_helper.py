import os
import json

def get_data_path(filename):
    """Get path to data file relative to this script"""
    return os.path.join(os.path.dirname(__file__), '..', 'data', filename)

def load_json(filename):
    """Load JSON file from data directory"""
    try:
        with open(get_data_path(filename), 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {filename} not found, returning empty dict")
        return {}
    except json.JSONDecodeError:
        print(f"Warning: {filename} is not valid JSON, returning empty dict")
        return {}

def save_json(filename, data):
    """Save JSON file to data directory"""
    os.makedirs(os.path.dirname(get_data_path(filename)), exist_ok=True)
    with open(get_data_path(filename), 'w') as f:
        json.dump(data, f, indent=2)

def append_to_json(filename, new_data):
    """Append data to existing JSON array"""
    current_data = load_json(filename)
    if isinstance(current_data, list):
        current_data.append(new_data)
    else:
        current_data = [current_data, new_data]
    save_json(filename, current_data)