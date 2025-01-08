from jwt.exceptions import ExpiredSignatureError as ExpiredSignatureError
from jwt.exceptions import InvalidTokenError as InvalidTokenError


class BaseAuthException(Exception):
    """Base exception for all exceptions in the ExiorAuth module."""

    pass


__all__ = ["BaseAuthException", "ExpiredSignatureError", "InvalidTokenError"]
