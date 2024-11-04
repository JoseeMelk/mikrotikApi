from utils.mikrotik_connection import MikroTikConnection

def add_user(username, password, group='read'):
    mikrotik_connection = MikroTikConnection()
    if not mikrotik_connection.is_connected():
        raise ConnectionError("No hay una conexión activa con MikroTik")

    api = mikrotik_connection.get_api()
    
    try:
        api.path('user').add(
            name=username,
            password=password,
            group=group
        )
        return {'status': 'success', 'message': f'Usuario {username} agregado correctamente'}
    except Exception as e:
        return {'status': 'error', 'message': f"Error al agregar usuario: {e}"}

def get_user_groups():
    mikrotik_connection = MikroTikConnection()
    if not mikrotik_connection.is_connected():
        raise ConnectionError("No hay una conexión activa con MikroTik")

    api = mikrotik_connection.get_api()
    
    try:
        groups = api.path('user/group').select('name')
        print(groups)
        group_list = [group['name'] for group in groups]
        return {'status': 'success', 'groups': group_list}
    except Exception as e:
        print(e)
        return {'status': 'error', 'message': f"Error al obtener grupos de usuarios: {e}"}
