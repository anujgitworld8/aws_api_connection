import os
import re
import hashlib
import secrets
import time
import binascii
from datetime import datetime, timezone, timedelta
from joserfc.jwt import JWTClaimsRegistry
from joserfc import jwt
from joserfc.errors import BadSignatureError, ExpiredTokenError, DecodeError
from passlib.context import CryptContext
from ..common.exceptions import exceptions
from ..common.json_responses import errormessages


# Class to authorize user.
class Auth:
    hasher = CryptContext(schemes=["bcrypt"])
    secretval = secrets.token_hex(32)

    os.environ["value"] = secretval

    secret = os.getenv("value")

    # Method to encode psswrd using sha512 algorithm and salt.
    def encode_psswrd(self, psswrd, salt):

        encoded_psswrd = psswrd.encode()
        digest = hashlib.pbkdf2_hmac("sha512", encoded_psswrd, salt, 10000)
        hex_hash = digest.hex()
        hashedpsswrd = hex_hash
        return hashedpsswrd

    # Method to encode token.
    def encode_token(self, userid):
        claims = {
            "sub": str(userid),
            "exp": datetime.now(timezone.utc) + timedelta(days=0, minutes=30),
            "iat": datetime.now(timezone.utc),
            "scope": "access_token",
        }
        headers = {"alg": "HS256"}
        return jwt.encode(headers, claims, self.secret)

    def decode_token(self, token):
        try:
            if not re.match(
                r"^[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+$", token
            ):
                raise ValueError(errormessages["errormessagecode"]["739"])

            time_now = int(time.time())
            obj = JWTClaimsRegistry()
            obj.now = time_now
            decoded_token = jwt.decode(token, self.secret, algorithms=["HS256"])
            obj.validate_exp(value=decoded_token.claims["exp"])
            if decoded_token.claims["scope"] == "access_token":
                return decoded_token.claims["sub"]
            exceptions(401, None, errormessages["errormessagecode"]["737"])

        except ExpiredTokenError:
            exceptions(401, None, errormessages["errormessagecode"]["738"])
        except (binascii.Error, BadSignatureError, DecodeError, ValueError):
            exceptions(401, None, errormessages["errormessagecode"]["739"])
