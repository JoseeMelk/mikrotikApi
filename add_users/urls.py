# authentication/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('add-user', add_user_view, name='add_user'),
    #path('mi/', login_mikrotik, name='mikrotik'),
]