from getajob.vendor.firestore.models import FirestoreFilters
from getajob.vendor.firestore.repository import FirestoreDB
from getajob.abstractions.repository import ParentRepository, RepositoryDependencies
from getajob.abstractions.models import Entity, EntityModels

from .models import Company

entity_models = EntityModels(entity=Company)


class CompanyRepository(ParentRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(
            RepositoryDependencies(db, Entity.COMPANIES.value, entity_models)
        )

    def get_companies_by_company_id_list(self, company_id_list: list[str]):
        return self.query(
            filters=[
                FirestoreFilters(
                    field="id", operator="in", value=company_id_list
                )
            ]
        )
