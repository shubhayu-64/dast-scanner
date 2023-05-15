from typing import List
from pydantic import BaseModel, Field
from datetime import datetime


class User(BaseModel):
    userId: str = Field(str, alias="userId")


class Alert(BaseModel):
    id: str = Field(..., alias="_id")
    userId: str = Field(..., alias="userId")
    url: str = Field(..., alias="url")
    name: str = Field(..., alias="name")
    risk: str = Field(..., alias="risk")
    cweid: str = Field(..., alias="cweid")
    description: str = Field(..., alias="description")
    reference: str = Field(..., alias="reference")
    solution: str = Field(..., alias="solution")


class Report(BaseModel):
    userId: str = Field(..., alias="userId")
    scanId: str = Field(..., alias="scanId")
    target: str = Field(..., alias="target")
    alerts: List[Alert] = Field(..., alias="alerts")
    status: str = Field(..., alias="status")
    createdAt: datetime = Field(..., alias="createdAt")
    updatedAt: datetime = Field(..., alias="updatedAt")


class History(BaseModel):
    userId: str = Field(..., alias="userId")
    scanId: str = Field(..., alias="scanId")
    target: str = Field(..., alias="target")
    status: str = Field(..., alias="status")
    createdAt: datetime = Field(..., alias="createdAt")
    updatedAt: datetime = Field(..., alias="updatedAt")
