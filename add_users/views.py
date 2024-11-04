from django.shortcuts import render, redirect
from .add_user_mtk import get_user_groups, add_user
from utils.mikrotik_connection import MikroTikConnection

def add_user_view(request):
    mikrotik_connection = MikroTikConnection()
    if not mikrotik_connection.is_connected():
        return redirect('login')
    
    group_data = get_user_groups()
    grups = group_data.get('groups', [])
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        group = request.POST.get('group', 'read')
        print(password)
        result = add_user(username, password, group)
        
        if result['status'] == 'success':
            return redirect('add_user')
        else:
            return render(request, 'add_users/add_user/add_user.html', {'error': result['message'],'groups': grups })

    return render(request, 'add_users/add_user/add_user.html', {'groups': grups})
