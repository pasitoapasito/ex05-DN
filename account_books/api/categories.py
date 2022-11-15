from ninja import Router

from typing import Optional, List

from django.http      import JsonResponse
from django.db.models import Q

from core.utils.auth import AuthBearer
from core.schema     import ErrorMessage

from account_books.schema import AccountBookCategoryCreateInput, AccountBookCategoryOutput
from account_books.models import AccountBookCategory


router = Router()


"""
가계부 카테고리 조회 API
"""
@router.get(
    '',
    tags     = ['3. 가계부 카테고리'],
    summary  = '가계부 카테고리 리스트 조회',
    response = List[AccountBookCategoryOutput],
    auth     = AuthBearer()
)
def get_list_account_book_categories(
    request,
    search: Optional[str] = None,
    sort  : str = 'up_to_date',
    status: str = 'deleted',
    offset: int = 0,
    limit : int = 10
    ):
    
    """
    JWT 토큰에서 유저정보 추출
    """
    user = request.auth

    """
    정렬 기준
    """
    sort_set = {
        'up_to_date' : '-created_at',
        'out_of_date': 'created_at'
    }
    
    """
    Q 객체 활용:
        - 검색 기능(가계부 카테고리 이름을 기준으로 검색 필터링)
        - 필터링 기능(본인의 카테고리 필터링)
    """
    q = Q()
    
    if search:
        q |= Q(name__icontains=search)
    if user:
        q &= Q(user=user)
    
    categories = AccountBookCategory.objects\
                                    .select_related('user')\
                                    .filter(q)\
                                    .exclude(status__iexact=status)\
                                    .order_by(sort_set[sort])[offset:offset+limit]
                                    
    return categories


"""
가계부 카테고리 생성 API
"""
@router.post(
    '',
    tags     = ['3. 가계부 카테고리'],
    summary  = '가계부 카테고리 생성',
    response = {200: AccountBookCategoryOutput, 400: ErrorMessage},
    auth     = AuthBearer()
)
def create_account_book_category(request, data: AccountBookCategoryCreateInput):
    
    """
    JWT 토큰에서 유저정보 추출
    """
    user = request.auth
    
    """
    가계부 카테고리 이름 필수값 확인
    """
    name = data.name
    if not name:
        return JsonResponse({'detail': '가계부 카테고리 이름은 필수 입력값입니다.'}, status=400)
    
    category = AccountBookCategory.objects\
                                  .create(
                                      user = user,
                                      name = name
                                  )
    return category