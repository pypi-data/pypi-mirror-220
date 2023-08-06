import json

from getajob.vendor.clerk.recruiters.repository import (
    WebhookCompanyMembershipRepository,
)
from getajob.vendor.clerk.recruiters.models import ClerkCompanyMembershipWebhookEvent


class RecruiterFixture:
    @staticmethod
    def create_recruiter_from_webhook(db):
        with open("tests/mocks/webhooks/create_recruiter.json", "r") as f:
            data = json.load(f)
        recruiter = ClerkCompanyMembershipWebhookEvent(**data)
        repo = WebhookCompanyMembershipRepository(db)
        return repo.create_recruiter(recruiter)
