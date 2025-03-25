from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class SUserAuth(BaseModel):
    email: EmailStr
    password: str
    is_admin: bool = False

    class Config:
        orm_mode = True