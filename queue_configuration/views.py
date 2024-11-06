from django.shortcuts import render, redirect

from .queue_config_mkt import set_bandwidth_limit, get_connected_devices, remove_bandwidth_limit
from utils.mikrotik_connection import MikroTikConnection

def show_queue(request):
    mikrotik_connection = MikroTikConnection()
    if not mikrotik_connection.is_connected():
        return redirect('login')

    if request.method == 'POST':
        target = request.POST.get('target')
        name = request.POST.get('name')
        upload = request.POST.get('upload')
        download = request.POST.get('download')

        #_target = f"{target}/{mask}"
        
        result = set_bandwidth_limit(target, name, download, upload)
        print(result)
        if result.get('status') == 'success':
            devices = get_connected_devices()
            return render(request, 'queue_configuration/queue/queue.html', {'devices': devices})
        else:
            devices = get_connected_devices()
            error_message = {'status': 'error', 'message': result.get('message')}
            return render(request, 'queue_configuration/queue/queue.html', {'error': error_message, 'devices': devices})
    devices = get_connected_devices()
    return render(request, 'queue_configuration/queue/queue.html', {'devices': devices})


def delete_queue(request, target):
    print(target)
    res = remove_bandwidth_limit(target)
    print(res)
    return redirect('show_queue')

