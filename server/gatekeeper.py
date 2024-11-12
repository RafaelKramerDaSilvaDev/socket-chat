import json

USERS_FILE = "./data/users.json"

def load_users():
    with open(USERS_FILE, "r") as file:
        data = json.load(file)
        return data["users"]

def authenticate(username, password):
    users = load_users()
    return username in users and users[username] == password
