from getajob.abstractions.models import Entity
from getajob.vendor.clerk.users.repository import WebhookUserRepository
from getajob.vendor.clerk.users.models import ClerkUserWebhookEvent
from getajob.contexts.users.resumes.repository import ResumeRepository
from getajob.contexts.users.resumes.models import CreateResume


class UserFixtures:
    @staticmethod
    def create_user_from_webhook(db):
        data = {
            "data": {
                "birthday": "",
                "created_at": 1654012591514,
                "email_addresses": [
                    {
                        "email_address": "example@example.org",
                        "id": "idn_29w83yL7CwVlJXylYLxcslromF1",
                        "linked_to": [],
                        "object": "email_address",
                        "verification": {"status": "verified", "strategy": "ticket"},
                    }
                ],
                "external_accounts": [],
                "external_id": "567772",
                "first_name": "Example",
                "gender": "",
                "id": "user_29w83sxmDNGwOuEthce5gg56FcC",
                "image_url": "https://img.clerk.com/xxxxxx",
                "last_name": "Example",
                "last_sign_in_at": 1654012591514,
                "object": "user",
                "password_enabled": True,
                "phone_numbers": [],
                "primary_email_address_id": "idn_29w83yL7CwVlJXylYLxcslromF1",
                "primary_phone_number_id": None,
                "primary_web3_wallet_id": None,
                "private_metadata": {},
                "profile_image_url": "https://www.gravatar.com/avatar?d=mp",
                "public_metadata": {},
                "two_factor_enabled": False,
                "unsafe_metadata": {},
                "updated_at": 1654012591835,
                "username": None,
                "web3_wallets": [],
            },
            "object": "event",
            "type": "user.created",
        }
        user = ClerkUserWebhookEvent(**data)
        repo = WebhookUserRepository(db)
        return repo.create_user(user)

    @staticmethod
    def create_user_resume(db, user_id: str):
        repo = ResumeRepository(db)
        return repo.create(
            data=CreateResume(resume="nice resume"),
            parent_collections={Entity.USERS.value: user_id},
        )
