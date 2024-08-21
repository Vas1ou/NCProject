from pydantic import BaseModel, EmailStr


# User Pydantic model
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str