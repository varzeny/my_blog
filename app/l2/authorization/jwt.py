# authorization/jwt.py

# lib
import jwt
from datetime import datetime, timezone, timedelta

# definition
def create_jwt(payload:dict, secret_key:str, algorithm:str)->str|None:
    try:
        encoded_token = jwt.encode(
            payload= payload,
            key= secret_key,
            algorithm= algorithm
        )
        return encoded_token
    except Exception as e:
        print("ERROR from create_jwt : ", e)
        return None


def verify_jwt(encoded_token:str, secret_key:str, algorithm:str)->dict|None:
    try:
        decoded_token = jwt.decode(
            jwt=encoded_token,
            key= secret_key,
            algorithms= algorithm
        )
        return decoded_token
    except jwt.ExpiredSignatureError:
        print("this Token has expired")
        return None
    except jwt.InvalidTokenError:
        print("this Token is Invalid token")
        return None
    except Exception as e:
        print("error from verify_token : ", e)
        return None  
