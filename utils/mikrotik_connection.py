from librouteros import connect

class MikroTikConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MikroTikConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self, username=None, password=None, host=None, port=8728):
        """Inicializa la conexión a MikroTik solo si aún no está conectada."""
        if not hasattr(self, 'api') or self.api is None:
            self.username = username
            self.password = password
            self.host = host
            self.port = port
            self.api = None

            # Si tenemos los datos de conexión, intentamos conectarnos automáticamente
            if self.username and self.password and self.host:
                self.connect()

    def connect(self):
        """Establece la conexión con MikroTik."""
        if not self.api:
            try:
                self.api = connect(
                    username=self.username,
                    password=self.password,
                    host=self.host,
                    port=self.port
                )
                print("Conexión establecida correctamente")
            except Exception as e:
                print(f"Error al conectar: {e}")
                self.api = None

    def is_connected(self):
        """Verifica si la conexión está establecida."""
        return self.api is not None

    def get_api(self):
        """Devuelve la API conectada, si está disponible."""
        return self.api if self.api else None

    def close(self):
        """Cierra la conexión si está activa."""
        if self.api:
            try:
                self.api.close()
                self.api = None
                print("Conexión cerrada correctamente")
            except Exception as e:
                print(f"Error al cerrar la conexión: {e}")
        else:
            print("No hay ninguna conexión activa para cerrar.")
