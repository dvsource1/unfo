import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def init_firebase():
    cred = credentials.Certificate('./firebase/firebase-service.json')
    return firebase_admin.initialize_app(cred)
    
def get_db():
    app = init_firebase()
    return firestore.client()