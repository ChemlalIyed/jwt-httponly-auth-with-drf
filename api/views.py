from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from django.http  import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.encoding import force_bytes
from .models import User
from.serializer import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.throttling import UserRateThrottle
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator,PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail,EmailMultiAlternatives,EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
default_token_generator = PasswordResetTokenGenerator()


def Template(request):
    return render(request,'index.html')

class Login(APIView):
     def post(self,request):
        password = request.data.get('password')
        email = request.data.get('email')
        print(email,password)
        usere = get_object_or_404(User,email=email)
        if not usere.is_active and usere.check_password(password):
                return Response({"detail": " not active go to email"}, status=status.HTTP_400_BAD_REQUEST)
        print(usere.username)
        user=authenticate(username=usere.username,password=password)
        print(user)
        if not usere:
                return Response({"detail": "Email not registered"}, status=status.HTTP_400_BAD_REQUEST)
        if user:
            token = RefreshToken.for_user(user)
            response = Response({"token":str(token.access_token)},status=status.HTTP_201_CREATED)
            response.set_cookie(
                key='access_token',
                value=str(token.access_token),
                httponly=True,
                secure=None,
                max_age=token.access_token.lifetime,
                samesite='Lax'
            )
            response.set_cookie(
                key='refresh_token',
                value=str(token),
                httponly=True,
                secure=None,
                max_age=token.lifetime,
                samesite='Lax'
            )
            return response
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
     
class Signup(APIView):
    def post(self,request):
        username=request.data.get("username")
        email=request.data.get("email")
        serilaize=UserSerializer(data=request.data)
        if serilaize.is_valid():
            serilaize.save()
            user=User.objects.get(username=username)
            token=default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            link = f"http://{get_current_site(request).domain}/api/activation/{uid}/{token}/"
            context={
                 "username":username,
                 "link":link
            }
            msg=EmailMultiAlternatives("Activaition link",from_email=settings.EMAIL_HOST_USER,to=[email])
            html_cont = render_to_string("email.html",context)
            msg.attach_alternative(html_cont,'text/html')
            msg.send(fail_silently=False)
            print("link:"+link)
            token = RefreshToken.for_user(user)
            response = Response({"token":str(token.access_token)},status=status.HTTP_201_CREATED)
            response.set_cookie(
                key='access_token',
                value=str(token.access_token),
                httponly=True,
                secure=None,
                max_age=token.access_token.lifetime,
                samesite='Lax'
            )
            response.set_cookie(
                key='refresh_token',
                value=str(token),
                httponly=True,
                secure=None,
                max_age=token.lifetime,
                samesite='Lax'
            )
            return response
        return Response({"errors":serilaize.error_messages})
class Getusers(ModelViewSet):
    throttle_classes=[]
    permission_classes=[IsAuthenticated]
    queryset=User.objects.all()
    serializer_class=UserSerializer    
# Create your views here.
class Is_auth(APIView):
    permission_classes=[AllowAny]
    def get(self,request):
        user =request.user
        print(user)
        if user.is_authenticated:
            return Response({"is_authenticated":True,"user":user.username})
        else:
            return Response({"is_authenticated":False})

class Logout(APIView):
    def get(self,request):
        response=Response({'logout':True})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response

class Togell(APIView):
    throttle_classes=[UserRateThrottle]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        return Response({"messege":"you did it wait 1 min"})
def active_user(request,uid,token):
    id=urlsafe_base64_decode(uid)
    try:
      user = User.objects.get(id=id)
    except Exception as e:
        user= None 
    if user and default_token_generator.check_token(user,token):    
      user.is_active=True
      user.save()
      return HttpResponse("active")
    else :
        return HttpResponse("Not active there is a error")