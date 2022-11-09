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