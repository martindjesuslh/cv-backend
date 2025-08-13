from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import List
from app.utils.validations import DateRange


class KeyCompetencies(BaseModel):
    title: str = Field(
        ..., min_length=5, max_length=60, description="Title of competence"
    )
    competences: List[str] = Field(default=[], description="All competences")


class ContactInfo(BaseModel):
    fullName: str = Field(..., min_length=3, max_length=100, description="Full name")
    address: str = Field(..., min_length=3, max_length=100, description="address valid")
    email: EmailStr = Field(..., description="Email valid")
    phone: str = Field(..., min_length=8, max_length=14, regex=r"^[\+]?[0-9\s\-\(\)]+$")
    whatsApp: str = Field(
        ..., min_length=8, max_length=14, regex=r"^[\+]?[0-9\s\-\(\)]+$"
    )


class WorkExperience(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Title of work")
    company_name: str = Field(
        ..., min_length=3, max_length=100, description="name of company"
    )
    date: DateRange
    where: str = Field(..., min_length=3, max_length=100, description="Title of work")
    responsibilities: List[str] = Field(..., min_length=1, max_length=30)


class Education(BaseModel):
    date: DateRange
    course_name: str = Field(
        ..., min_length=3, max_length=100, description="Title of work"
    )
    description: str = Field(
        ..., min_length=3, max_length=100, description="Title of work"
    )


class CvInfo(BaseModel):
    header: ContactInfo
    profile_profesional: str = Field(..., min_length=10, max_length=300)
    key_competences: List[KeyCompetencies] = Field(..., min_length=1, max_length=20)
    work_experience: List[WorkExperience] = Field(..., min_length=1, max_length=20)
    education: List[Education] = Field(..., min_length=1, max_length=20)


class Payload(BaseModel):
    cv: CvInfo
    profiles: List[HttpUrl]
