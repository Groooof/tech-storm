from pydantic import BaseModel


class TokensSchema(BaseModel):
    access_token: str
    refresh_token: str


class AccessTokenPayload(BaseModel):
    user_id: int
    exp: int


class RefreshTokensRequestSchema(BaseModel):
    refresh_token: str


class RefreshTokensSchema(BaseModel):
    user_id: int
    refresh_token: str


class LogoutSchema(BaseModel):
    user_id: int
    refresh_token: str
