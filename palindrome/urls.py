from django.urls import path, re_path, include
from .views import home, redirect, get_access, user_info

urlpatterns = [
    path('', home, name="home"),
    path('redirect', redirect, name='redirect'),
    path('get-access', get_access, name='get-access'),
    path('user-info', user_info, name='user_info'),
]