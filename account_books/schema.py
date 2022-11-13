from datetime import date, datetime
from typing   import Optional
from decimal  import Decimal

from ninja    import Schema


class AccountBookCreateInput(Schema):
    name  : str
    budget: Decimal
    status: Optional[str] = 'in_use'


class AccountBookCreateOutput(Schema):
    id      : int
    nickname: str
    name    : str
    budget  : Decimal
    status  : str

    @staticmethod
    def resolve_nickname(obj):
        if not obj.user.nickname:
            return None
        return obj.user.nickname