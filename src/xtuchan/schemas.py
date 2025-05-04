from pydantic import BaseModel


class TuchanBase(BaseModel):
    class Config:
        orm_mode = True
        from_attributes = True
        arbitrary_types_allowed = True