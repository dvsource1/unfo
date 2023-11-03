from firebase.base import get_db

db = get_db()


def add_entry(collection: str, data: dict):
  return db.collection(collection).add(data)


def set_entry(collection: str, doc_id: str, data: dict):
  return db.collection(collection).document(str(doc_id)).set(data)
