from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RefreshAuthRequest(_message.Message):
    __slots__ = ("cookie", "tenant_id")
    COOKIE_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    cookie: str
    tenant_id: str
    def __init__(self, cookie: _Optional[str] = ..., tenant_id: _Optional[str] = ...) -> None: ...

class RefreshAuthResponse(_message.Message):
    __slots__ = ("is_valid", "auth_token")
    IS_VALID_FIELD_NUMBER: _ClassVar[int]
    AUTH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    is_valid: bool
    auth_token: str
    def __init__(self, is_valid: bool = ..., auth_token: _Optional[str] = ...) -> None: ...
