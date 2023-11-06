from firebase.base import get_db

db = get_db()


def get_entries(collection: str, with_subcollections=False):
  if with_subcollections:
    documents = db.collection_group(collection).stream()

    final_list = []
    for doc in documents:
      doc_dict = doc.to_dict()
      subcollections = doc.reference.collections()
      
      for subcollection in subcollections:
        subcollection_name = subcollection.id
        subcollection_docs = subcollection.stream()
        doc_dict[subcollection_name] = [subcollection_doc.to_dict() for subcollection_doc in subcollection_docs]
      final_list.append(doc_dict)
    return final_list
    
  return [doc.to_dict() for doc in db.collection(collection).stream()]


def add_entry(collection: str, data: dict):
  return db.collection(collection).add(data)


def set_entry(collection: str, doc_id: str, data: dict):
  return db.collection(collection).document(str(doc_id)).set(data)
