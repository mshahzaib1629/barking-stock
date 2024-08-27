import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def initialize_firebase():
    cred = credentials.Certificate('./firebase_service_account.json')
    app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase Initialized!")
    return app, db