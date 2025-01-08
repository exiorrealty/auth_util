import pathlib
from pydantic_settings import BaseSettings
import jwt


class Secrets(BaseSettings):
    KEY_PATH: pathlib.Path
    JWT_ALGORITHM: str = "RS256"
    JWT_MAX_AGE: int = 300


class _JWTUtil:
    def __init__(
        self,
        key_path: pathlib.Path = Secrets().KEY_PATH,
        algorithm: str = Secrets().JWT_ALGORITHM,
        max_age: int = Secrets().JWT_MAX_AGE,
        issuer: str = "exior-web",
    ):
        self.key_path = key_path
        self.algorithm = algorithm
        self.max_age = max_age
        self.issuer = issuer

    def create_jwt(self, data: dict):
        """
        Generate a JWT with given data and expiration time.
        """
        private_key = self.key_path / "private"
        if not private_key.exists():
            raise FileNotFoundError(f"Private key not found")
        to_encode = data.copy()
        to_encode.update({"iss": self.issuer})
        encoded_jwt = jwt.encode(payload=to_encode, key=private_key.read_bytes(), algorithm=self.algorithm)
        return encoded_jwt

    def validate_jwt(self, token: str):
        public_key = self.key_path / "public"

        # validate keys
        if not public_key.exists():
            raise FileNotFoundError(f"Public key not found")

        payload = jwt.decode(jwt=token, key=public_key.read_bytes(), algorithms=[self.algorithm])
        return payload

    @staticmethod
    def decode_jwt(token: str) -> dict:
        return jwt.decode(token, verify=False)


jwt_util = _JWTUtil()
