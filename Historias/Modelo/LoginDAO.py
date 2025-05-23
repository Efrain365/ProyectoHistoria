from .Conexion import ConexionDB

class LoginDAO_:
    def __init__(self):
        self.db = ConexionDB()

    def validar_credenciales(self, usuario, password):
        """Valida si las credenciales existen en la base de datos."""
        try:
            # Usar la conexión existente
            cursor = self.db.cursor

            # Consulta para buscar el usuario y la contraseña
            cursor.execute("SELECT * FROM usuarios WHERE Nombre = ? AND Contraseña = ?", (usuario, password))
            resultado = cursor.fetchone()

            return resultado is not None  # True si las credenciales son válidas, False de lo contrario

        except Exception as e:
            print(f"Error al validar credenciales: {e}")
            return False
        finally:
            self.db.cerrarConexion()
