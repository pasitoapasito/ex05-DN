import re

from ninja                  import Router
from django.http            import JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from users.schema import UserSignUpInput, UserSignUpOutput
from users.models import User


router = Router()


"""
유저 회원가입 API
"""
@router.post(
    '/signup',
    tags     = ['1. 유저'],
    response = UserSignUpOutput,
    summary  = "유저 회원가입"
)
def user_signup(request, data: UserSignUpInput):
    email = data.email
    if not email:
        return JsonResponse({'detail': '이메일은 필수 입력값입니다.'}, status=400)
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'detail': '이메일 형식이 잘못되었습니다.'}, status=400)
    if User.objects.filter(email=email).exists():
        return JsonResponse({'detail': f'{email}은/는 이미 존재합니다.'}, status=400)
    
    password = data.password
    if not password:
        return JsonResponse({'detail': '패스워드는 필수 입력값입니다.'}, status=400)
    """
    패스워드 조건: 길이 8~20 자리, 최소 1개 이상의 소문자, 대문자, 숫자, (숫자키)특수문자로 구성
    """
    password_regex = '^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,20}$'
    if not re.match(password_regex, password):
        return JsonResponse({'detail': '올바른 비밀번호를 입력하세요.'}, status=400)
    
    nickname = data.nickname
    if not nickname:
        return JsonResponse({'detail': '닉네임은 필수 입력값입니다.'}, status=400)
    if User.objects.filter(nickname=nickname).exists():
        return JsonResponse({'detail': f'{nickname}은/는 이미 존재합니다.'}, status=400)
    
    user = User.objects\
               .create_user(
                   email    = data.email,
                   nickname = data.nickname,
                   password = password
               )
    
    return user