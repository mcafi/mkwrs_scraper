import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('./mariokart-dfb9b-firebase-adminsdk-60yys-451a2bfc6f.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

def add_data(data, game, record_type = "complete"):
    doc_ref = db.collection("track_records").document(game)
    subcollection_ref = doc_ref.collection(record_type)
    subcollection_ref.add(data)