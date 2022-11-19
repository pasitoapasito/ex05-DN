import re, jwt

from ninja    import Router
from datetime import datetime, timedelta

from django.http                 import JsonResponse
from django.core.validators      import validate_email
from django.core.exceptions      import ValidationError
from django.contrib.auth.hashers import check_password

from users.schema    import UserSignUpInput, UserSignUpOutput, UserSignInInput, UserSignInOutput
from users.models    import User
from config.settings import SECRET_KEY


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
    
    """
    이메일 필수값/중복/형식 확인
    """
    email = data.email
    if not email:
        return JsonResponse({'detail': '이메일은 필수 입력값입니다.'}, status=400)
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'detail': '이메일 형식이 잘못되었습니다.'}, status=400)
    if User.objects.filter(email=email).exists():
        return JsonResponse({'detail': f'{email}은/는 이미 존재합니다.'}, status=400)
    
    """
    패스워드 필수값/형식 확인
    패스워드 조건: 길이 8~20 자리, 최소 1개 이상의 소문자, 대문자, 숫자, (숫자키)특수문자로 구성
    """
    password = data.password
    if not password:
        return JsonResponse({'detail': '패스워드는 필수 입력값입니다.'}, status=400)
    password_regex = '^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,20}$'
    if not re.match(password_regex, password):
        return JsonResponse({'detail': '올바른 비밀번호를 입력하세요.'}, status=400)
    
    """
    닉네임 필수값/중복 확인
    """
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


"""
유저 로그인 API
"""
@router.post(
    '/signin',
    tags     = ['1. 유저'],
    response = UserSignInOutput,
    summary  = "유저 로그인"
)
def user_signin(request, data: UserSignInInput):
    
    """
    이메일/패스워드 필수값 확인
    """
    email = data.email
    if not email:
        return JsonResponse({'detail': '이메일은 필수 입력값입니다.'}, status=400)
    password = data.password
    if not password:
        return JsonResponse({'detail': '패스워드는 필수 입력값입니다.'}, status=400)
    
    """
    입력받은 이메일 정보와 매칭되는 유저객체 추출
    """
    try:
        user = User.objects.values('id', 'password').get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'detail': '올바른 유저정보를 입력하세요.'}, status=400)
    
    """
    입력받은 패스워드가 유저의 패스워드와 일치하는지 확인
    """
    if not check_password(password, user['password']):
        return JsonResponse({'detail': '올바른 유저정보를 입력하세요.'}, status=400)
    
    """
    액세스/리프레시 토큰 발급
    토큰 만료기간: 액세스 토큰(1일), 리프레시 토큰(7일) 
    """
    now = datetime.now()
    
    access_token_exp_date  = now + timedelta(days=1)
    refresh_token_exp_date = now + timedelta(days=7)
    
    access_token = jwt.encode(
        {
            'user_id' : user['id'],
            'exp_date': str(access_token_exp_date)
        },
        SECRET_KEY,
        algorithm = 'HS256'
    )
    refresh_token = jwt.encode(
        {
            'user_id' : user['id'],
            'exp_date': str(refresh_token_exp_date)
        },
        SECRET_KEY,
        algorithm = 'HS256'
    )

    return JsonResponse(
        {
            'access_token' : access_token,
            'refresh_token': refresh_token
        },
        status=200
    )