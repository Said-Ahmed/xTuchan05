from typing import Optional

from pydantic import BaseModel, EmailStr

class SUserRegister(BaseModel):
    email: EmailStr
    password: str
    is_admin: bool = False

    class Config:
        orm_mode = True


class SUserAuth(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True