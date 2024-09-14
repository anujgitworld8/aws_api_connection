# backend/src/auth/authentication.py

import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException

class Auth:
    secret = "your_secret_key"

    def encode_token(self, user_id):
        payload = {
            "exp": datetime.utcnow() + timedelta(days=1),
            "iat": datetime.utcnow(),
            "sub": user_id
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
