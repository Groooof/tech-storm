from typing import Any

from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    def __init__(
        self, status_code: int = status.HTTP_401_UNAUTHORIZED, detail: Any = "Could not validate credentials"
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers={"WWW-Authenticate": "Bearer"})
