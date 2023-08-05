import logging

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes, HTTPBearer
from jose import jwt, JWTError

__all__ = ["JWTBearer", "get_security", "CredentialsException", "check_token_and_scopes"]


class JWTBearer(HTTPBearer):
    async def __call__(self, *args, **kwargs) -> str | None:
        result = await super().__call__(*args, **kwargs)
        if result is None:
            return None
        return result.credentials


def get_security(
    token_url: str | None = None,
    auto_error: bool = True,
    scheme_name: str | None = None,
    description: str | None = None
):
    if token_url is None:
        return JWTBearer(auto_error=auto_error, scheme_name=scheme_name, description=description)
    else:
        return OAuth2PasswordBearer(
            tokenUrl=token_url, auto_error=auto_error, scheme_name=scheme_name, description=description
        )


class CredentialsException(HTTPException):
    def __init__(self, authenticate_value="bearer") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value}
        )


def check_token_and_scopes(
    security_scopes: SecurityScopes, token: str, key: str | dict, algorithms: str | list
) -> int:
    if security_scopes.scopes:
        authenticate_value = f"bearer scope={security_scopes.scope_str}"
    else:
        authenticate_value = "bearer"
    try:
        payload = jwt.decode(token, key, algorithms=algorithms)
        user_id: int = int(payload["sub"])
        token_scopes = set(payload["scope"].split(" "))
        for scope in security_scopes.scopes:
            if scope not in token_scopes:
                raise CredentialsException(authenticate_value)
        return user_id
    except (JWTError, KeyError, ValueError):
        logging.error("Invalid JWT token during authentication")
        raise CredentialsException(authenticate_value)
