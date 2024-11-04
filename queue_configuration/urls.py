from django.urls import path
from .views import *

urlpatterns = [
    path('show-queue/', show_queue, name='show_queue'),
]