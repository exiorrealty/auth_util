from typing import Literal

from pydantic import BaseModel

class TokenUserInfo(BaseModel):
    user_id: str
    user_type: Literal["root", "sso", "native"] = "native"
    tenant_id: str
    project_id: str