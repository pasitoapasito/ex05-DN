from ninja import Router

from django.http      import JsonResponse
from django.db.models import Q
from typing           import Optional, List

from core.utils           import AuthBearer
from account_books.schema import AccountBookCreateInput, AccountBookOutput
from account_books.models import AccountBook


router = Router()


"""
가계부 조회 API
"""
@router.get(
    '',
    tags     = ['2. 가계부'],
    summary  = '가계부 리스트 조회',
    response = List[AccountBookOutput],
    auth     = AuthBearer()
)
def get_list_account_book(
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
            'out_of_date': 'created_at',
            'high_budget': '-budget',
            'low_budget' : 'budget'
    }

    """
    Q 객체 활용:
        - 검색 기능(가계부 이름을 기준으로 검색 필터링)
        - 필터링 기능(본인의 가계부 필터링)
    """
    q = Q()

    if search:
        q |= Q(name__icontains=search)           
    if user:
        q &= Q(user=user)

    books = AccountBook.objects\
                       .select_related('user')\
                       .filter(q)\
                       .exclude(status__iexact=status)\
                       .order_by(sort_set[sort])[offset:offset+limit]

    return books


"""
가계부 생성 API
"""
@router.post(
    '',
    tags     = ['2. 가계부'],
    summary  = '가계부 생성',
    response = AccountBookOutput,
    auth     = AuthBearer()
)
def create_account_book(request, data: AccountBookCreateInput):
    """
    JWT 토큰에서 유저정보 추출
    """
    user = request.auth

    """
    가계부 이름/예산 필수값 확인
    """
    name = data.name
    if not name:
        return JsonResponse({'detail': '가계부 이름은 필수 입력값입니다.'}, status=400)
    budget = data.budget
    if budget is None:
        return JsonResponse({'detail': '가계부 예산은 필수 입력값입니다.'}, status=400)

    book = AccountBook.objects\
                      .create(
                            user   = user,
                            name   = name,
                            budget = budget
                      )       
    return book