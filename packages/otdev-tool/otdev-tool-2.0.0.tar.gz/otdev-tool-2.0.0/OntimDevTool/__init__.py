import json
G_version = "2.0.0"
G_auth_server = "http://192.168.12.81:8888/"
G_secure_access = True

if not G_secure_access:
    G_auth_server += "no_auth/"

with open('authorization.json', 'r') as f:
    authorization = json.load(f)
    G_password = authorization["password"]

def get_password():
    return G_password

def set_password(password):
    global G_password
    G_password = password