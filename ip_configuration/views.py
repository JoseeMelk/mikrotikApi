from django.http import JsonResponse
from django.shortcuts import render, redirect
from utils.mikrotik_connection import MikroTikConnection
from .ip_config_mkt import assign_ip_to_interface, get_interface, get_ip_addresses, get_ip_address, remove_ip, disable_interface

def show_interface(request):
    mikrotik_connection = MikroTikConnection()
    if not mikrotik_connection.is_connected():
        return redirect('login') 
    try:
        interfaces = get_interface()
        filtered_interfaces = [
            {
                'id': interface.get('.id'),
                'name': interface.get('name'),
                'running': interface.get('running'),
                'disabled': interface.get('disabled'),
                'mac_address': interface.get('mac-address')
            }
            for interface in interfaces
        ]

        context = {
                'interfaces': filtered_interfaces
            }

        return render(request, 'ip_configuration/show_interface/show_interface.html', context)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error al consultar interfaces: {e}'})

'''
# Nueva vista para habilitar/deshabilitar la interfaz
def toggle_interface(request, interface_id):
    mikrotik_connection = MikroTikConnection()
    if not mikrotik_connection.is_connected():
        return JsonResponse({'status': 'error', 'message': 'No conectado a MikroTik'})

    try:
        # Obtener el estado actual de la interfaz
        interfaces = get_interface()
        interface = next((i for i in interfaces if i.get('.id') == interface_id), None)

        if interface:
            # Habilitar o deshabilitar la interfaz según su estado actual
            if interface.get('disabled'):
                enable_interface(interface_id)
            else:
                disable_interface(interface_id)

            return JsonResponse({'status': 'success', 'message': 'Interfaz actualizada correctamente'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Interfaz no encontrada'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error al cambiar estado de la interfaz: {e}'})
'''
def show_ip(request):
    mikrotik_connection = MikroTikConnection()
    if not mikrotik_connection.is_connected():
        return redirect('login')

    try:
        ip_addresses = get_ip_addresses()
        formatted_ip_addresses = [
                {
                    'id': ip.get('.id'),
                    'address': ip.get('address'),
                    'network': ip.get('network'),
                    'interface': ip.get('interface'),
                    'invalid': ip.get('invalid'),
                    'dynamic': ip.get('dynamic'),
                    'disabled': ip.get('disabled')
                }
                for ip in ip_addresses
            ]

        context = {
            'ip_addresses': formatted_ip_addresses,
        }
        return render(request, 'ip_configuration/show_ip/show_ip.html', context)
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})
    
def add_ip(request):
    mikrotik_connection = MikroTikConnection()
    if not mikrotik_connection.is_connected():
        return redirect('login')

    if request.method == 'POST':
        interface_name = request.POST.get('interfaceSelect')
        ip_address = request.POST.get('ipInput')
        subnet_mask = request.POST.get('subnetMask')

        result = assign_ip_to_interface(interface_name, ip_address, subnet_mask)
        if result.get('status') == 'success':
            return redirect('show_ip')
        else:
            error_message = {'status': 'error', 'message': result.get('message')}
            return render(request, 'error.html', {'error': error_message})
    try:
        interfaces = get_interface()
        filtered_interfaces = [
            {
                'id': interface.get('.id'),
                'name': interface.get('name'),
            }
            for interface in interfaces
        ]

        context = {
            'interfaces':filtered_interfaces,
        }

        return render(request, 'ip_configuration/add_ip/add_ip.html', context)
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})
    
def delete_ip(request, interface_name):
    mikrotik_connection = MikroTikConnection()
    if not mikrotik_connection.is_connected():
        return redirect('login')
    if request.method == 'POST':
        try:
            ip_addresses = get_ip_addresses()
            ip = get_ip_address(interface_name, ip_addresses)
            remove_ip(ip_addresses, ip)
            return redirect('show_ip')
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error al eliminar la IP: {str(e)}'})
    else:
        return redirect('show_ip')
