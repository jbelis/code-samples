import requests


def take_a_risk():
    try:
        risky_operation()
    except Exception as e:
        print("An error occurred!")

def risky_operation():
    raise Exception("This is too risky!")


def read_file(file_path) -> str:
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found."
    

def fetch_data():
    try:
        return requests.get("http://example.com").json()
    except Exception:
        return {}