from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework import status
class Refreshfromcookies(TokenRefreshView):
    throttle_classes=[]
    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get('refresh_token')
        if not refresh:
            return Response({"Authntication":"Token not found"},status=status.HTTP_401_UNAUTHORIZED)
        request.data['refresh']=refresh
        res= super().post(request, *args, **kwargs)
        if res.status_code == 200:
            new_access = res.data.get('access')
            a=AccessToken(new_access)
            print(a)
            response = Response({"Authntication":"Token refreshed"},status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=str(new_access),
                httponly=True,
                secure=None,
                expires=a['exp'],
                samesite='Lax'
            )
            return response
        return res