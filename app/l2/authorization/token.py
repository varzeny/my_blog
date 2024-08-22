# authorization/token.py

# lib
from datetime import datetime, timezone, timedelta

# definition
class Token:
    secret_key:str = None
    algorithm:str = None
    exp_min:float = None

    def __init__(self, sub:str, exp:int) -> None:
        self.sub = sub
        self.exp = exp if exp!=None else ( datetime.now(timezone.utc)+timedelta(minutes=self.exp_min) ).timestamp()

    def extend_token(self):
        self.exp = ( datetime.now(timezone.utc) + timedelta(minutes=self.exp_min) ).timestamp()
    
    @classmethod
    def setup(cls, config:dict):
        cls.secret_key = config["secret_key"]
        cls.algorithm = config["algorithm"]
        cls.exp_min = config["exp_min"]


class AccessToken(Token):
    def __init__(self, sub="access_token", exp=None, account_id_=None, account_role_="guest") -> None:
        super().__init__(sub, exp)
        self.account_id_=account_id_
        self.account_role_=account_role_

