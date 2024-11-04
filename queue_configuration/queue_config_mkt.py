from utils.mikrotik_connection import MikroTikConnection

def get_connected_devices():
    """
    Obtiene una lista de dispositivos conectados a MikroTik con sus límites de ancho de banda.
    
    Retorna:
    - Lista de diccionarios con las direcciones IP, MAC, y límites de subida y bajada de los dispositivos conectados.
    """
    mikrotik_connection = MikroTikConnection()
    if not mikrotik_connection.is_connected():
        raise ConnectionError("No hay una conexión activa con MikroTik")

    api = mikrotik_connection.get_api()
    
    try:
        # Obtener la lista de dispositivos conectados desde la tabla ARP
        devices = api.path('ip','dhcp-server','lease').select('address')
        queues = api.path("queue","simple")
        x =tuple(queues)
        print(x)
        connected_devices = []
        for d in devices:
            ip = d.get("address")

            for q in x:
                target = q.get("target")
                if target.len():
                    print('vacio')
                    break
                ip_target = target.split("/")
                if ip_target[0] == ip:
                    data = q.get("max-limit")
                    max_limit = data.split("/")
                    print(max_limit)
        

            
            
        return connected_devices
    except Exception as e:
        print(e)
        return {'status': 'error', 'message': f"Error al obtener dispositivos conectados: {e}"}


def set_bandwidth_limit(target, max_limit_download, max_limit_upload):
    """
    Configura el límite de ancho de banda en MikroTik utilizando colas simples.
    
    Parámetros:
    - target: IP o nombre de la interfaz a la que se aplicará el límite.
    - max_limit_download: Límite máximo de descarga (en bits por segundo).
    - max_limit_upload: Límite máximo de subida (en bits por segundo).
    
    Ejemplo de uso:
    set_bandwidth_limit('192.168.88.10', '2M', '1M')  # Limita a 2 Mbps de descarga y 1 Mbps de subida.
    """
    mikrotik_connection = MikroTikConnection()
    if not mikrotik_connection.is_connected():
        raise ConnectionError("No hay una conexión activa con MikroTik")

    api = mikrotik_connection.get_api()
    
    try:
        max=f"{max_limit_upload}M/{max_limit_download}M" 
        print(max)
        api.path("queue","simple").add(
            name=f"limit_{target}",  # Nombre de la queue
            target=target,           # IP o interfaz objetivo
            **{'max-limit':max}  # Límite de subida/descarga
        )
        '''

        api.path("/queue/simple").add({
            'name': f'tt_{target}',
            'target': target,
            'max-limit':max
        })
'''
        return {'status': 'success', 'message': 'Ancho de banda configurado correctamente'}
    except Exception as e:
        return {'status': 'error', 'message': f"Error al configurar el ancho de banda: {e}"}
    


