from ninja import Router

from django.http import JsonResponse

from core.utils  import AuthBearer


router = Router()


@router.get(
    '/auth-test',
    tags     = ['2. 테스트'],
    summary  = "인증/인가 테스트",
    auth     = AuthBearer()
)
def test(request):
    user = request.auth
    return JsonResponse({'msg': f'{user.nickname}는 인증/인가에 통과했습니다.'}, status=200)