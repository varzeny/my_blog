# authorization/__init__.py

# lib
from pydantic import BaseModel, Field
from typing import Literal
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from fastapi import HTTPException

# module
from .token import *
from .jwt import *
from .hash import *

# attribution
__all__ = [
    
]

CONFIG = {}

# method
def setup(config:dict):
    global CONFIG
    CONFIG=config

    # access_token
    AccessToken.setup( CONFIG["access_token"] )


def get_token_from_cookie(req:Request, token_name:str)->dict|None:
    try:
        encoded_token = req.cookies.get(token_name)
        if encoded_token:
            decoded_token = verify_jwt(
                encoded_token=encoded_token,
                secret_key=CONFIG[token_name]["secret_key"],
                algorithm=CONFIG[token_name]["algorithm"]
            )
            if decoded_token:
                return decoded_token
            else:
                return None
        else:
            raise Exception(f"{token_name} does't exsit")
    except Exception as e:
        print("ERROR from get_token_from_cookie : ", e)
        return None


def put_token_to_cookie(resp:Response, token:Token):
    try:
        resp.set_cookie(
            key=token.sub,
            value=create_jwt(
                payload=token.__dict__,
                secret_key=token.secret_key,
                algorithm=token.algorithm
            ),
            httponly=True,
            secure=True,
            path="/",
            max_age=token.exp_min*60
        )
        return resp
    except Exception as e:
        print("ERROR from put_token_to_cookie : ", e)
        return None


# dependency
def admin_only(req:Request):
    if req.state.access_token.account_role_ == "admin":
        return
    else:
        raise HTTPException(status_code=401, detail="wrong access")
