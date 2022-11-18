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
    price: Decimal
    description: str
    category_id: int
    book_id    : int
    

class AccountBookLogUpdateInput(Schema):
    title: Optional[str] = None
    types: Optional[str] = None
    price: Optional[Decimal] = None
    description: Optional[str] = None    
    book_id    : int
    category_id: int


class AccountBookLogCreateUpdateOutput(Schema):
    id   : int
    title: str
    types: str
    price: Decimal
    description: str
    status     : str
    book       : str
    category   : Optional[str] = None
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
    price: Decimal
    description: str
    status     : str
    book       : str
    category   : Optional[str] = None
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
    expected_budget  : Decimal
    total_income     : Optional[Decimal] = None
    total_expenditure: Optional[Decimal] = None
    logs: Optional[List[AccountBookLogOutput]] = None