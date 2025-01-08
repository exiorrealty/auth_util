import os

import grpc
from auth_util import refresh_token_pb2_grpc as pb2_grpc
from auth_util import refresh_token_pb2 as pb2


def refresh_auth_token(cookie: str, tenant_id: str) -> str | None:
    with grpc.insecure_channel(os.getenv("GRPC_AUTH_SERVICE_URL", "localhost:50051")) as channel:
        stub = pb2_grpc.AuthServiceStub(channel)
        message = pb2.RefreshAuthRequest(cookie=cookie, tenant_id=tenant_id)
        resp = stub.RefreshAuthToken(message)
        if resp.is_valid:
            return resp.auth_token
        else:
            return None
