from firebase.base import get_db

db = get_db()


def add_entry(collection: str, data: dict):
  db.collection(collection).add(data)
  