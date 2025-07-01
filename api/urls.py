from django.urls import path
from .views import Login,Signup,Test,Template,Logout,active_user
from .refresh import Refreshfromcookies
urlpatterns=[
    path("login/",Login.as_view()),
    path("signup/",Signup.as_view()),
    path("logout/",Logout.as_view()),
    path("protected_view/",Test.as_view({'get': 'list'})),
    path("token/refresh/",Refreshfromcookies.as_view()),
    path("",Template),
    path("activation/<uid>/<str:token>/",active_user),

]