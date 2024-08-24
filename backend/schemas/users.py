from pydantic import BaseModel


class UserAuthSchema(BaseModel):
    username: str
    password: str


class UserInfoSchema(BaseModel):
    id: int
    username: str
