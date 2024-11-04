from django.urls import path
from .views import *

urlpatterns = [
    path('show-interface/', show_interface, name='show_interface'),
    path('add-ip/', add_ip, name='add_ip'),
    path('delete-ip/<str:interface_name>/', delete_ip, name='delete_ip'),
    path('show-ip/', show_ip, name='show_ip'),
    #path('toggle/<str:interface_id>/', toggle_interface, name='toggle_interface'),
    #path('mi/', login_mikrotik, name='mikrotik'),
]