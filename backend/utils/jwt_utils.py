import jwt  # ✅ This is the PyJWT library
import datetime

SECRET_KEY = "your-secret-key"  # You should load this from environment in production!

def create_token(data: dict, expires_in: int = 3600) -> str:
    payload = data.copy()
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}


# 1. data.copy() → user data (जैसे {"user_id": 123}) payload में डाला जाएगा।

#  "exp" field → token expire होने का time (UTC + given seconds)।
# 2. Default = 3600 sec = 1 hour.

#  jwt.encode(...) → HS256 algorithm से signed token string generate करता है।

