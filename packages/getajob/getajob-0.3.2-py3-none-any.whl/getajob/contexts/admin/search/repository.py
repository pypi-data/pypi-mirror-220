from getajob.abstractions.repository import query_collection
from getajob.vendor.firestore.repository import FirestoreDB

from .models import AdminEntitySearch


class AdminSearchRepository:
    def __init__(self, db: FirestoreDB):
        self.db = db

    def admin_collection_search(self, search: AdminEntitySearch):
        return query_collection(db=self.db, collection_name=search.entity_type.value)
