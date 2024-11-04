# middleware/mikrotik_middleware.py

from utils.mikrotik_connection import MikroTikConnection

class MikroTikConnectionMiddleware:
    """
    Middleware para mantener la conexión a MikroTik si ya está establecida.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Si la conexión ya existe en la sesión, la restauramos
        if 'mikrotik_connection' in request.session:
            connection_data = request.session['mikrotik_connection']
            mikrotik_connection = MikroTikConnection(
                username=connection_data['username'],
                password=connection_data['password'],
                host=connection_data['host'],
                port=connection_data['port']
            )
            mikrotik_connection.connect()
            request.mikrotik_connection = mikrotik_connection
        else:
            request.mikrotik_connection = None

        # Procesamos la respuesta
        response = self.get_response(request)

        # Después de la respuesta, cerramos la conexión si fue creada
        if request.mikrotik_connection:
            request.mikrotik_connection.close()

        return response
