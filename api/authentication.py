from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken,TokenError,AuthenticationFailed
class JWTcookieauth(JWTAuthentication):
    def authenticate(self, request):
        access_token= request.COOKIES.get('access_token')
        if access_token:
              validated_token=self.get_validated_token(access_token)
              return self.get_user(validated_token),validated_token
        return None