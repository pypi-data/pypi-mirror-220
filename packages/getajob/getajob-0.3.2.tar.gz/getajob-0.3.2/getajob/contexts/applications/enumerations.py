from enum import Enum


class ApplicationStatus(str, Enum):
    draft = "draft"
    submitted = "submitted"
    accepted = "accepted"
    rejected = "rejected"
    withdrawn = "withdrawn"
