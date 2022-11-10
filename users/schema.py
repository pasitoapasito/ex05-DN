from datetime import date, datetime
from typing   import Optional

from ninja    import Schema


class UserSignUpInput(Schema):
    email   : str
    nickname: str
    password: str


class UserSignUpOutput(Schema):
    id      : int
    email   : str
    nickname: str
    

class UserSignInInput(Schema):
    email   : str
    password: str
    

class UserSignInOutput(Schema):
    access_token : str
    refresh_token: str