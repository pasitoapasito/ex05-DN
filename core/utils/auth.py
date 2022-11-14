import jwt

from ninja.security  import HttpBearer
from datetime        import datetime
from typing          import Union, Any

from config.settings import SECRET_KEY
from users.models    import User


class AuthBearer(HttpBearer):
    def authenticate(self, request, token: str) -> Union[Any, bool]:
        
        try:
            """
            JWT 토큰 decode
            """
            payload = jwt.decode(
                token, 
                SECRET_KEY, 
                algorithms = 'HS256'
            )
            user_id  = payload['user_id']
            exp_date = payload['exp_date']
            
            """
            JWT 토큰 만료기간 확인
            """
            token_exp_date = datetime.strptime(
                exp_date, 
                '%Y-%m-%d %H:%M:%S.%f'
            )
            if datetime.now() > token_exp_date:
                return False
            
            """
            JWT 토큰 유저정보 확인
            """
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return False
            
            return user
        
        except Exception as e:
            print(e)
            return False