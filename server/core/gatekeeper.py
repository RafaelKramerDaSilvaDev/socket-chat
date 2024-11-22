from constants.users import USERS

def authenticate(username, password):
    return username in USERS and USERS[username] == password
