from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class MacBase(SQLModel):
    name: str = Field(default="unknown")
    public_ip: str = Field(default="127.0.1.1")
    status: str = Field(default="stopped")
    memory: int = Field(default=0)
    mac_os: str = Field(default="OpenTofu 2.3.1")


class MacOS(MacBase):
    # __tablename__ = "macs"
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)


class MacPublic(MacBase):
    id: UUID
