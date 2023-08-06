import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore as f
from firebase_admin.firestore import firestore
from firebase_admin.exceptions import FirebaseError
from firebase_admin.auth import TokenSignError
import os

from firebase_admin import auth

def create_firebase_user(email, password) -> 'auth.UserRecord':
    try:
        return auth.create_user(email=email, password=password)
    except ValueError as e:
        raise e
    except FirebaseError as e:
        raise e;  

def create_firebase_custom_token(uid) -> 'auth.UserRecord':
    try:
        return auth.create_custom_token(uid)
    except ValueError as e:
        raise e
    except TokenSignError as e:
        raise e;  

DEFAULT_PATH = os.environ.get('FIREBASE_CREDENTIALS_PATH');

def initializeApp(path: str):
    if path is None:
        return None;
    try:
        absolute_path = os.path.dirname(__file__)
        relative_path = path
        credentials_path = os.path.join(absolute_path, relative_path)
        cred = credentials.Certificate(credentials_path);
        if len(firebase_admin._apps)==0:
            app = firebase_admin.initialize_app(cred);
            return app;
        return firebase_admin.get_app()
    except Exception as e:
        print(e)
        return None
    
class FirestoreApp:
    def __init__(self, credentials_path: str=DEFAULT_PATH) -> None:
        # print("Initializing Firestore from", credentials_path)
        app = initializeApp(credentials_path);
        if app is not None:
            self.app = app;
            
    
    def firestore_client(self) -> firestore.Client:
        app = getattr(self, 'app', None)
        if app is None:
            return None;
        firestore_database = f.client(self.app);
        return firestore_database;
