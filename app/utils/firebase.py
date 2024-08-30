import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

def _find_project_root(current_path, marker_files=('.git', 'setup.py', 'requirements.txt')):
    # Keep traversing up until we find a known project file or directory
    while current_path != os.path.dirname(current_path):  # While we haven't reached the top
        if any(os.path.exists(os.path.join(current_path, marker)) for marker in marker_files):
            return current_path
        current_path = os.path.dirname(current_path)
    
    return None

def initialize_firebase():
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    project_root_path = _find_project_root(current_file_path)
    firebase_creds_path = os.path.join(project_root_path, 'firebase_service_account.json')

    cred = credentials.Certificate(firebase_creds_path)
    app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase Initialized!")
    return app, db