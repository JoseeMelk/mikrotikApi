from django.shortcuts import render, redirect

from .queue_config_mkt import set_bandwidth_limit, get_connected_devices
from utils.mikrotik_connection import MikroTikConnection

def show_queue(request):
    mikrotik_connection = MikroTikConnection()
    if not mikrotik_connection.is_connected():
        return redirect('login')

    if request.method == 'POST':
        target = request.POST.get('target')
        upload = request.POST.get('upload')
        download = request.POST.get('download')
        
        result = set_bandwidth_limit(target, download, upload)
        print(result)
        if result.get('status') == 'success':
            devices = get_connected_devices()
            return render(request, 'queue_configuration/queue/queue.html', {'devices': devices})
        else:
            error_message = {'status': 'error', 'message': result.get('message')}
            return render(request, 'error.html', {'error': error_message})
    devices = get_connected_devices()
    return render(request, 'queue_configuration/queue/queue.html', {'devices': devices})

