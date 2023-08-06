import os
import json
import hashlib
G_version = "2.0.4"
G_auth_server = "http://192.168.12.81:8888/"
G_secure_access = True

if not G_secure_access:
    G_auth_server += "no_auth/"

authfile = "authorization.json"
if os.path.exists(authfile):
    with open(authfile, 'r') as f:
        authorization = json.load(f)
        G_password = authorization["password"]
else:
    # create default password
    with open(authfile, "w") as f:
        md5 = hashlib.md5("123456".encode("ascii"))
        G_password = md5.hexdigest()
        authorization = {"password": G_password}
        json.dump(authorization, f)

def get_password():
    return G_password

def set_password(password):
    global G_password
    G_password = password