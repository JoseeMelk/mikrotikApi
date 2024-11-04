from django.shortcuts import render, redirect
from django.http import JsonResponse
from utils.mikrotik_connection import MikroTikConnection

def login_view(request):
    mikrotik_connection = MikroTikConnection()
    if mikrotik_connection.is_connected():
        return redirect('/')
    
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        host = request.POST.get('host')
        port = request.POST.get('port')

        if username and password and host and port:
            mikrotik_connection = MikroTikConnection(
                username=username,
                password=password,
                host=host,
                port=port
            )
            
            if not mikrotik_connection.is_connected():
                mikrotik_connection.connect()

            api = mikrotik_connection.get_api()

            if api:
                return redirect('index')
            else:
                return JsonResponse({'status': 'error', 'message': 'Failed to connect to MikroTik'})
        else:
            return JsonResponse({'status': 'error', 'message': 'All fields are required'})

    return render(request, 'authentication/login/login.html')

def close(request):
    mikrotik_connection = MikroTikConnection()
    if mikrotik_connection.is_connected():
        mikrotik_connection.close()
    return redirect('login')

def index(request):
    mikrotik_connection = MikroTikConnection()

    if not mikrotik_connection.is_connected():
        return redirect('login')
    return render(request, "ip_configuration/index/index.html")


