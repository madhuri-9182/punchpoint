# app/schemas.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime, date


class EmployeeCreate(BaseModel):
    name: str
    email: str
    password: str


class EmployeeOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    active: bool

    model_config = ConfigDict(from_attributes=True)


class LoginSchema(BaseModel):
    email: str
    password: str


class AttendanceOut(BaseModel):
    id: int
    date: date
    login_time: datetime | None
    logout_time: datetime | None
    
    model_config = ConfigDict(from_attributes=True)
