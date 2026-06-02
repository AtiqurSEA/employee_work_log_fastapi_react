from datetime import date
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=72)


class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    role: str

    class Config:
        from_attributes = True


class WorkLogBase(BaseModel):
    date: date
    task: str = Field(min_length=1, max_length=255)
    hours: float = Field(gt=0)
    status: str
    project: str = Field(min_length=1, max_length=100)
    comments: str | None = None


class WorkLogCreate(WorkLogBase):
    pass


class WorkLogUpdate(WorkLogBase):
    pass


class WorkLogOut(WorkLogBase):
    id: int
    user_id: int
    user_full_name: str | None = None

    class Config:
        from_attributes = True
