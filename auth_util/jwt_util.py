import pathlib

import jwt
from pydantic_settings import BaseSettings


class _Secrets(BaseSettings):
    KEY_PATH: pathlib.Path
    JWT_ALGORITHM: str = "RS256"
    JWT_MAX_AGE: int = 300

__secrets__ = _Secrets()

class _JWTUtil:
    def __init__(
        self,
        key_path: pathlib.Path = __secrets__.KEY_PATH,
        algorithm: str = __secrets__.JWT_ALGORITHM,
        max_age: int = __secrets__.JWT_MAX_AGE,
        issuer: str = "exior-web",
    ):
        self.key_path = key_path
        self.algorithm = algorithm
        self.max_age = max_age
        self.issuer = issuer

    def create_jwt(self, data: dict):
        """Generate a JWT with given data and expiration time."""
        private_key = self.key_path / "private"
        if not private_key.exists():
            raise FileNotFoundError("Private key not found")
        to_encode = data.copy()
        to_encode.update({"iss": self.issuer})
        encoded_jwt = jwt.encode(payload=to_encode, key=private_key.read_bytes(), algorithm=self.algorithm)
        return encoded_jwt

    def validate_jwt(self, token: str):
        public_key = self.key_path / "public"

        # validate keys
        if not public_key.exists():
            raise FileNotFoundError("Public key not found")

        payload = jwt.decode(jwt=token, key=public_key.read_bytes(), algorithms=[self.algorithm])
        return payload

    @staticmethod
    def decode_jwt(token: str) -> dict:
        return jwt.decode(token, verify=False)


jwt_util = _JWTUtil()
