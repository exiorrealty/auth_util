from typing import Literal

from pydantic import BaseModel


class TokenUserInfo(BaseModel):
    user_id: str
    privilege: Literal["root", "tenant_admin", "project_admin", "user"]
    tenant_id: str
    project_id: str