from ninja import Router

from typing import Optional

from django.http      import HttpRequest, JsonResponse
from django.db.models import Q, Sum

from core.schema                    import ErrorMessage
from core.utils.auth                import AuthBearer
from core.utils.get_obj_n_check_err import GetAccountBook, GetAccountBookCategory, GetAccountBookLog

from account_books.schema import AccountBookLogCreateInput, AccountBookLogUpdateInput, AccountBookLogCreateUpdateOutput, AccountBookLogListOutput
from account_books.models import AccountBookLog


router = Router()


"""
가계부 기록 조회 API
"""
@router.get(
    '',
    tags     = ['4. 가계부 기록'],
    summary  = '가계부 기록 리스트 조회',
    response = AccountBookLogListOutput,
    auth     = AuthBearer()
)
def get_list_account_book_log(
    request    : HttpRequest,
    book_id    : int,
    cateogry_id: Optional[str] = None,
    search     : Optional[str] = None,
    types      : Optional[str] = None,
    sort       : str = 'up_to_date',
    status     : str = 'deleted',
    offset     : int = 0,
    limit      : int = 10
    ) -> JsonResponse:
    
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
        'high_price' : '-price',
        'low_price'  : 'price',    
    }
    
    """
    가계부 id 필수값 확인
    """
    account_book_id = book_id
    if not account_book_id:
        return JsonResponse({'detail': '가계부는 필수 입력값입니다.'}, status=400)
    
    """
    가계부 객체/유저정보 확인
    """
    book, err = GetAccountBook.get_book_n_check_error(account_book_id, user)
    if err:
        return JsonResponse({'detail': err}, status=400)
    
    """
    Q 객체 활용:
        - 검색 기능(가계부 기록 제목/설명/카테고리를 기준으로 검색 필터링)
        - 필터링 기능(가계부 기록 카테고리/타입을 기준으로 필터링)
        - 필터링 기능(본인의 가계부 기록 필터링)
    """
    q = Q()
    
    if search:
        q |= Q(title__icontains = search)
        q |= Q(description__icontains = search)
        q |= Q(category__name__icontains = search)
    if account_book_id:
        q &= Q(book_id = book.id)
    if cateogry_id:
        categories = cateogry_id.split(',')
        q &= Q(category_id__in = categories)
    if types:
        q &= Q(types__iexact = types)
        
    logs = AccountBookLog.objects\
                         .select_related('category', 'book')\
                         .filter(q)\
                         .exclude(status__iexact=status)\
                         .order_by(sort_set[sort])
    
    """
    총수입/총지출 기록 산출
    """                      
    income      = logs.filter(types='income').aggregate(total=Sum('price'))
    expenditure = logs.filter(types='expenditure').aggregate(total=Sum('price'))
    
    """
    가계부 기록 반환 데이터(페이지네이션 기능 포함)
    """
    data = {
        'nickname'         : user.nickname,
        'expected_budget'  : book.budget,
        'total_income'     : income['total'],
        'total_expenditure': expenditure['total'],
        'logs'             : list(logs)[offset:offset+limit]
    }
    
    return data
    

"""
가계부 기록 생성 API
"""
@router.post(
    '',
    tags     = ['4. 가계부 기록'],
    summary  = '가계부 기록 생성',
    response = {200: AccountBookLogCreateUpdateOutput, 400: ErrorMessage},
    auth     = AuthBearer()
)
def create_account_book_log(
    request: HttpRequest,
    data   : AccountBookLogCreateInput
    ) -> JsonResponse:
    
    """
    JWT 토큰에서 유저정보 추출
    """
    user = request.auth
    
    """
    필수값 확인:
        - 가계부 id
        - 가계부 카테고리 id
        - 가계부 기록 제목/타입/가격/설명
    """
    account_book_id = data.book_id
    if not account_book_id:
        return JsonResponse({'detail': '가계부는 필수 입력값입니다.'}, status=400)
    account_book_category_id = data.category_id
    if not account_book_category_id:
        return JsonResponse({'detail': '가계부 카테고리는 필수 입력값입니다.'}, status=400)
    title = data.title
    if not title:
        return JsonResponse({'detail': '가계부 기록 제목은 필수 입력값입니다.'}, status=400)
    types = data.types
    if not types:
        return JsonResponse({'detail': '가계부 기록 타입은 필수 입력값입니다.'}, status=400)
    price = data.price
    if price is None:
        return JsonResponse({'detail': '가계부 기록 가격은 필수 입력값입니다.'}, status=400)
    description = data.description
    if not description:
        return JsonResponse({'detail': '가계부 기록 설명은 필수 입력값입니다.'}, status=400)
    
    """
    가계부 객체/유저정보 확인
    """
    book, err = GetAccountBook.get_book_n_check_error(account_book_id, user)
    if err:
        return JsonResponse({'detail': err}, status=400)
    
    """
    가계부 카테고리 객체/유저정보 확인
    """
    category, err = GetAccountBookCategory.get_category_n_check_error(account_book_category_id, user)
    if err:
        return JsonResponse({'detail': err}, status=400)
    
    log = AccountBookLog.objects\
                        .create(
                            book        = book,
                            category    = category,
                            title       = title,
                            price       = price,
                            description = description,
                            types       = types               
                        ) 
    return log    


"""
가계부 기록 수정 API
"""
@router.patch(
    '/{int:account_book_log_id}',
    tags     = ['4. 가계부 기록'],
    summary  = '가계부 기록 수정',
    response = {200: AccountBookLogCreateUpdateOutput, 400: ErrorMessage},
    auth     = AuthBearer()
)
def update_account_book_log(
    request: HttpRequest,
    data   : AccountBookLogUpdateInput,
    account_book_log_id: int
    ) -> JsonResponse:
    
    """
    JWT 토큰에서 유저정보 추출
    """
    user = request.auth
    
    """
    필수값 확인:
        - 가계부 id
        - 가계부 카테고리 id
        - 가계부 기록 id
    """
    account_book_id = data.book_id
    if not account_book_id:
        return JsonResponse({'detail': '가계부는 필수 입력값입니다.'}, status=400)
    account_book_category_id = data.category_id
    if not account_book_category_id:
        return JsonResponse({'detail': '가계부 카테고리는 필수 입력값입니다.'}, status=400)
    if not account_book_log_id:
        return JsonResponse({'detail': '가계부 기록은 필수 입력값입니다.'}, status=400)

    """
    가계부 객체/유저정보 확인
    """
    book, err = GetAccountBook.get_book_n_check_error(account_book_id, user)
    if err:
        return JsonResponse({'detail': err}, status=400)

    """
    가계부 카테고리 객체/유저정보 확인
    """
    category, err = GetAccountBookCategory.get_category_n_check_error(account_book_category_id, user)
    if err:
        return JsonResponse({'detail': err}, status=400)

    """
    가계부 기록 객체/유저정보 확인
    """
    log, err = GetAccountBookLog.get_log_n_check_error(account_book_log_id, book, user)
    if err:
        return JsonResponse({'detail': err}, status=400)

    if data.title:
        log.title = data.title
    if data.types:
        log.types = data.types
    if data.price is None:
        log.price = data.price
    if data.description:
        log.description = data.description
    if data.category_id:
        log.category = category

    log.save()

    return log


"""
가계부 기록 삭제 API
"""
@router.delete(
    '/{int:account_book_log_id}',
    tags     = ['4. 가계부 기록'],
    summary  = '가계부 기록 삭제',
    response = {204: None, 400: ErrorMessage},
    auth     = AuthBearer()
)
def delete_account_book_log(
    request: HttpRequest,
    account_book_id    : int,
    account_book_log_id: int,
    ) -> JsonResponse:
    
    """
    JWT 토큰에서 유저정보 추출
    """
    user = request.auth

    """
    필수값 확인:
        - 가계부 id
        - 가계부 기록 id
    """
    if not account_book_id:
        return JsonResponse({'detail': '가계부는 필수 입력값입니다.'}, status=400)
    if not account_book_log_id:
        return JsonResponse({'detail': '가계부 기록은 필수 입력값입니다.'}, status=400)
    
    """
    가계부 객체/유저정보 확인
    """
    book, err = GetAccountBook.get_book_n_check_error(account_book_id, user)
    if err:
        return JsonResponse({'detail': err}, status=400)

    """
    가계부 기록 객체/유저정보 확인
    """
    log, err = GetAccountBookLog.get_log_n_check_error(account_book_log_id, book, user)
    if err:
        return JsonResponse({'detail': err}, status=400)

    if log.status == 'deleted':
        return JsonResponse({'detail': f'가계부 기록 {account_book_log_id}(id)는 이미 삭제된 상태입니다.'}, status=400)

    log.status = 'deleted'
    log.save()

    return 204, None


"""
가계부 기록 복구 API
"""
@router.patch(
    '/{int:account_book_log_id}/restore',
    tags     = ['4. 가계부 기록'],
    summary  = '가계부 기록 복구',
    response = {204: None, 400: ErrorMessage},
    auth     = AuthBearer()
)
def restore_account_book_log(
    request: HttpRequest,
    account_book_id    : int,
    account_book_log_id: int,
    ) -> JsonResponse:
    
    """
    JWT 토큰에서 유저정보 추출
    """
    user = request.auth

    """
    필수값 확인:
        - 가계부 id
        - 가계부 기록 id
    """
    if not account_book_id:
        return JsonResponse({'detail': '가계부는 필수 입력값입니다.'}, status=400)
    if not account_book_log_id:
        return JsonResponse({'detail': '가계부 기록은 필수 입력값입니다.'}, status=400)
    
    """
    가계부 객체/유저정보 확인
    """
    book, err = GetAccountBook.get_book_n_check_error(account_book_id, user)
    if err:
        return JsonResponse({'detail': err}, status=400)

    """
    가계부 기록 객체/유저정보 확인
    """
    log, err = GetAccountBookLog.get_log_n_check_error(account_book_log_id, book, user)
    if err:
        return JsonResponse({'detail': err}, status=400)

    if log.status == 'in_use':
        return JsonResponse({'detail': f'가계부 기록 {account_book_log_id}(id)는 이미 사용중입니다.'}, status=400)

    log.status = 'in_use'
    log.save()

    return 204, None