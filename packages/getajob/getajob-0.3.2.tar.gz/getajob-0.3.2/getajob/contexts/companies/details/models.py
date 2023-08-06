from pydantic import BaseModel

from getajob.abstractions.models import BaseDataModel

from ..enumerations import NumEmployeesEnum


class CreateCompanyDetails(BaseModel):
    num_employees: NumEmployeesEnum | None = None
    owner_first_and_last_name: str | None = None
    owner_phone_number: str | None = None
    company_description: str | None = None


class CompanyDetails(BaseDataModel, CreateCompanyDetails):
    ...
