from utils.mikrotik_connection import MikroTikConnection

def convert_to_units(value):
    # Units in descending order
    units = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB']
    
    def convert_size(bytes):
        # Convert to float to handle precise divisions
        bytes = float(bytes)
        
        i = 0
        while bytes >= 1024 and i < len(units) - 1:
            bytes /= 1024.0
            i += 1
        
        # Return the value formatted with the corresponding unit
        return f"{bytes:.2f} {units[i]}"
    
    # Convert all values in the list
    return convert_size(value)

def convert_to_units_sb(_value):
    value = int(_value)
    # Verifica si el valor es menor que 1 MB (se convierte a KB o Bytes)
    if value < 1:
        # Si el valor es menor que 1MB, convertir primero a Bytes
        value_in_bytes = value * 1024 * 1024  # Convertir a Bytes
        if value_in_bytes < 1024:
            return f"{int(value_in_bytes)}B"  # Si es menos de 1KB, devolver en Bytes
        else:
            value_in_kb = value_in_bytes / 1024  # Convertir a KB
            return f"{int(value_in_kb)}K"  # Si es menor a 1MB, devolver en KB
    elif value < 1024:
        # Si el valor es entre 1MB y 1024MB, devolver en MB
        return f"{int(value)}M"
    elif value < 1024 * 1024:
        # Si el valor es entre 1GB y 1024GB, devolver en GB
        value_in_gb = value / 1024
        return f"{int(value_in_gb)}G"
    elif value < 1024 * 1024 * 1024:
        # Si el valor es entre 1TB y 1024TB, devolver en TB
        value_in_tb = value / (1024 * 1024)
        return f"{int(value_in_tb)}T"
    else:
        # Si el valor es mayor a 1TB, lo devolveremos en TB
        return f"{int(value)}T"

def get_connected_devices():
    mikrotik_connection = MikroTikConnection()
    if not mikrotik_connection.is_connected():
        raise ConnectionError("No hay una conexión activa con MikroTik")

    api = mikrotik_connection.get_api()
    
    try:
        # Obtener la lista de dispositivos conectados desde la tabla ARP
        devices = api.path('ip','dhcp-server','lease').select('address')
        queues = api.path("queue","simple")
        x =tuple(queues)
        queue_list = []

        if not x:
            print({'status':'empty', 'message':'not queue'})
            return None
        formatted_queues = [
            {
                'ip_address': q.get("target").split("/")[0],  # IP address (antes de la barra "/")
                'netmask': q.get("target").split("/")[1],     # Netmask (después de la barra "/")
                'name': q.get("name"),
                'upload_limit': convert_to_units(q.get("max-limit").split("/")[0]),  # Límite de subida
                'download_limit': convert_to_units(q.get("max-limit").split("/")[1])  # Límite de bajada
            }
            for q in queues
        ]  
        print(formatted_queues)      
        return formatted_queues
    except Exception as e:
        print(e)
        return {'status': 'error', 'message': f"Error al obtener dispositivos conectados: {e}"}


def set_bandwidth_limit(target, _name, max_limit_download, max_limit_upload):
    mikrotik_connection = MikroTikConnection()
    if not mikrotik_connection.is_connected():
        raise ConnectionError("No hay una conexión activa con MikroTik")

    api = mikrotik_connection.get_api()
    
    try:
        print(convert_to_units_sb(max_limit_upload))
        print(convert_to_units_sb(max_limit_download))
        max=f"{max_limit_upload}M/{max_limit_download}M" 
        print(max)
        api.path("queue","simple").add(
            name=_name,  # Nombre de la queue
            target=target,           # IP o interfaz objetivo
            **{'max-limit':max}  # Límite de subida/descarga
        )
        return {'status': 'success', 'message': 'Ancho de banda configurado correctamente'}
    except Exception as e:
        return {'status': 'error', 'message': f"Error al configurar el ancho de banda: {e}"}
    
def remove_bandwidth_limit(target):
    """
    Elimina el límite de ancho de banda (cola) configurado en MikroTik para una IP o interfaz específica.
    
    Parámetros:
    - target: IP o nombre de la interfaz a la que se le eliminará el límite.
    
    Ejemplo de uso:
    remove_bandwidth_limit('192.168.88.10')  # Elimina la cola asociada a la IP '192.168.88.10'.
    """
    mikrotik_connection = MikroTikConnection()
    
    if not mikrotik_connection.is_connected():
        raise ConnectionError("No hay una conexión activa con MikroTik")

    api = mikrotik_connection.get_api()

    try:
        # Obtener la lista de todas las colas simples configuradas
        queues = api.path("queue", "simple")
        
        # Buscar la cola que tenga como target la IP proporcionada
        for queue in queues:
            print(queue)
            _target = queue.get('target').split('/')
            if _target[0] == target:
                # Encontramos la cola, la eliminamos
                api.path("queue", "simple").remove(queue['.id'])
                return {'status': 'success', 'message': f'Cola para {target} eliminada correctamente.'}
        
        # Si no encontramos ninguna cola para esa IP, devolvemos un mensaje informativo
        return {'status': 'error', 'message': f'No se encontró una cola para la IP {target}.'}
    
    except Exception as e:
        return {'status': 'error', 'message': f"Error al eliminar la cola: {e}"}


