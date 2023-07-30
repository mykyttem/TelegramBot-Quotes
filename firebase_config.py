import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("name_file.json")
firebase_admin.initialize_app(cred, {"databaseURL": "url"})

ref = db.reference('/')