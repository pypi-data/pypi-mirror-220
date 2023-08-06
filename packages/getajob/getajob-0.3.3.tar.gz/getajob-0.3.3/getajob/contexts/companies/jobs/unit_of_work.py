from getajob.abstractions.repository import BaseRepository
from getajob.abstractions.models import Entity

from .models import CreateJob, UserCreateJob


class JobsUnitOfWork:
    def __init__(self, job_repo: BaseRepository):
        self.repo = job_repo

    def create_job(self, company_id: str, data: UserCreateJob):
        new_job = CreateJob(**data.dict(), view_count=0)
        # Other business logic here
        return self.repo.create(
            new_job, parent_collections={Entity.COMPANIES.value: company_id}
        )
