from datetime import datetime

from ninja import Schema
from pydantic import BaseModel


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    created: datetime
    updated: datetime

    class Config:
        from_attributes = True


class TodoCreate(BaseModel):
    title: str
    description: str


class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Message(Schema):
    detail: str


class Token(Schema):
    message: str
    token: str
