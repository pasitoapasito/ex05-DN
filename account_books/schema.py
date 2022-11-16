from typing  import Optional, List
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


class AccountBookCategoryUpdateInput(Schema):
    name: Optional[str] = None
    

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
    
    
class AccountBookLogCreateInput(Schema):
    title: str
    types: str
    price: int
    description: str
    cateogry_id: int
    book_id    : int
    
    
class AccountBookLogCreateOutput(Schema):
    id   : int
    title: str
    types: str
    price: int
    description: str
    status     : str
    book       : str
    category   : str
    created_at : str
    updated_at : str
    
    @staticmethod
    def resolve_book(obj):
        return obj.book.name
    
    @staticmethod
    def resolve_category(obj):
        if obj.category.status == 'deleted':
            category = None
        else:
            category = obj.category.name
        return category
    
    @staticmethod
    def resolve_created_at(obj):
        return (obj.created_at).strftime('%Y-%m-%d %H:%M')
    
    @staticmethod
    def resolve_updated_at(obj):
        return (obj.updated_at).strftime('%Y-%m-%d %H:%M')
    
    
class AccountBookLogOutput(Schema):
    id   : int
    title: str
    types: str
    price: int
    description: str
    status     : str
    book       : str
    category   : str
    created_at : str
    updated_at : str
    
    @staticmethod
    def resolve_book(obj):
        return obj.book.name
    
    @staticmethod
    def resolve_category(obj):
        if obj.category.status == 'deleted':
            category = None
        else:
            category = obj.category.name
        return category
    
    @staticmethod
    def resolve_created_at(obj):
        return (obj.created_at).strftime('%Y-%m-%d %H:%M')
    
    @staticmethod
    def resolve_updated_at(obj):
        return (obj.updated_at).strftime('%Y-%m-%d %H:%M')
    
    
class AccountBookLogListOutput(Schema):
    nickname         : str
    expected_budget  : int
    total_income     : Optional[int] = None
    total_expenditure: Optional[int] = None
    logs: Optional[List[AccountBookLogOutput]] = None