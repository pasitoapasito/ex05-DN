from typing  import Optional
from decimal import Decimal

from ninja import Schema


class AccountBookCreateInput(Schema):
    name  : str
    budget: Decimal
    status: Optional[str] = 'in_use'


class AccountBookUpdateInput(Schema):
    name  : Optional[str] = None
    budget: Optional[Decimal] = None


class AccountBookOutput(Schema):
    id      : int
    nickname: Optional[str] = None
    name    : str
    budget  : Decimal
    status  : str

    @staticmethod
    def resolve_nickname(obj):
        if not obj.user.nickname:
            return None
        return obj.user.nickname
    

class AccountBookCategoryCreateInput(Schema):
    name  : str
    status: Optional[str] = 'in_use'


class AccountBookCategoryOutput(Schema):
    id      : int
    nickname: Optional[str] = None
    name    : str
    status  : str
    
    @staticmethod
    def resolve_nickname(obj):
        if not obj.user.nickname:
            return None
        return obj.user.nickname