from ninja import Router

from django.http import JsonResponse

from core.utils           import AuthBearer
from account_books.schema import AccountBookCreateInput, AccountBookCreateOutput
from account_books.models import AccountBook


router = Router()


"""
가계부 생성 API
"""
@router.post(
    '',
    tags     = ['2. 가계부'],
    summary  = "가계부 생성",
    response = AccountBookCreateOutput,
    auth     = AuthBearer()
)
def create_account_book(request, data: AccountBookCreateInput):
    user = request.auth

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