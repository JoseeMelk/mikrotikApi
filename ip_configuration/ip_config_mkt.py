from utils.mikrotik_connection import MikroTikConnection

def get_interface():
    mikrotik_connection = MikroTikConnection()
    if not mikrotik_connection.is_connected():
        raise ConnectionError("No hay una conexión activa con MikroTik")

    api = mikrotik_connection.get_api()
    try:
        interface = api.path('interface')
        return interface
    except Exception as e:
        raise RuntimeError(f"Error al obtener interfaces: {e}")

def is_exist_interface(interface_name):
    try:
        interface = get_interface()
        for _interface in interface:
            if _interface.get('name') == interface_name:
                return True
    except Exception as e:
        raise RuntimeError(f"Error al verificar existencia de la interfaz: {e}")
    
    return False

def enable_interface(interface_id):
    connection = MikroTikConnection().get_connection()
    connection('/interface', 'enable', {'numbers': interface_id})

def disable_interface(interface_id):
    connection = MikroTikConnection().get_connection()
    connection('/interface', 'disable', {'numbers': interface_id})

def get_ip_addresses():
    mikrotik_connection = MikroTikConnection()
    if not mikrotik_connection.is_connected():
        raise ConnectionError("No hay una conexión activa con MikroTik")
    
    api = mikrotik_connection.get_api()
    try:
        ip_addresses = api.path('ip/address')
        return ip_addresses
    except Exception as e:
        raise RuntimeError(f"Error al obtener direcciones IP: {e}")

def get_ip_address(interface_name, ip_addresses):
    try:
        for ip in ip_addresses:
            if ip.get('interface') == interface_name:
                return ip
    except Exception as e:
        raise RuntimeError(f"Error al obtener la IP de la interfaz: {e}")
    
    return None 

def remove_ip(ip_addresses, ip):
    if ip:
        try:
            ip_addresses.remove(ip.get('.id'))
        except Exception as e:
            raise RuntimeError(f"Error al eliminar IP: {e}")
    else:
        raise ValueError("No IP found to remove.")

def assign_ip_to_interface(interface_name, ip_address, mask):
    mikrotik_connection = MikroTikConnection()
    if not mikrotik_connection.is_connected():
        raise ConnectionError("No hay una conexión activa con MikroTik")
    if not is_exist_interface(interface_name):
        return {'status': 'not exist', 'message': 'No existe la interfaz'}

    ip_address = f"{ip_address}/{mask}"
    ip_addresses = get_ip_addresses()
    
    ip = get_ip_address(interface_name, ip_addresses)
    if ip:
        remove_ip(ip_addresses, ip)
    try:
        ip_addresses.add(
            interface=interface_name,
            address=ip_address
        )
        return {'status': 'success', 'message': 'IP asignada correctamente'}
    except Exception as e:
        return {'status': 'error', 'message': f"Error al asignar IP: {e}"}