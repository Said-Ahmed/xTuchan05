from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class SUserRegister(BaseModel):
    email: EmailStr
    password: str
    is_admin: bool = False

    model_config = ConfigDict(from_attributes=True)


class SUserAuth(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)