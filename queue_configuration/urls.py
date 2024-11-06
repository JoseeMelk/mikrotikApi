from django.urls import path
from .views import *

urlpatterns = [
    path('show-queue/', show_queue, name='show_queue'),
    path('delete-queue/<str:target>/', delete_queue, name='delete_queue'),
]