import json

from fastapi import HTTPException, Request, Response, status
from auth_util.jwt_util import jwt_util
from pydantic import BaseModel

from auth_util.exceptions import ExpiredSignatureError, InvalidTokenError
from auth_util.refresh_auth_token import refresh_auth_token


class TokenUserInfo(BaseModel):
    user_id: str
    tenant_id: str
    project_id: str


COOKIE_AUTH_TOKEN = "auth-token"
COOKIE_REFRESH_TOKEN = "refresh-token"


def authenticate(request: Request, response: Response):
    """Dependency to authenticate a user using a JWT stored in a cookie."""
    # Retrieve the token from the cookie
    auth_token = request.cookies.get(COOKIE_AUTH_TOKEN)
    refresh_token = request.cookies.get(COOKIE_REFRESH_TOKEN)
    if not auth_token or not refresh_token:
        raise HTTPException(status_code=401, detail="Authentication or Refresh token missing")
    try:
        # Decode and validate the JWT
        payload = jwt_util.validate_jwt(auth_token)
        return TokenUserInfo(
            user_id=payload["user_id"],
            tenant_id=payload["tenant_id"],
            project_id=payload["project_id"],
        )
    except ExpiredSignatureError:
        # If the token has expired, try to refresh it
        unverified_payload = jwt_util.decode_jwt(auth_token)
        new_auth_token = refresh_auth_token(
            cookie=json.dumps(request.cookies),
            tenant_id=unverified_payload["tenant_id"],
        )
        if not new_auth_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token invalid or expired, please login again.",
            )

        response.set_cookie("auth-token", new_auth_token)
        payload = jwt_util.validate_jwt(new_auth_token)
        return TokenUserInfo(
            user_id=payload["user_id"],
            tenant_id=payload["tenant_id"],
            project_id=payload["project_id"],
        )
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
