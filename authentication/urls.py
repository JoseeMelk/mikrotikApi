# authentication/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('close/', close, name='close'),
    #path('mi/', login_mikrotik, name='mikrotik'),
]