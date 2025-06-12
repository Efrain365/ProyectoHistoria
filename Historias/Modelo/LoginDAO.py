from .Conexion import ConexionDB

class LoginDAO_:
    def __init__(self):
        self.db = ConexionDB()

    def validar_credenciales(self, usuario, password):
        """Valida si las credenciales existen en la base de datos."""
        try:
            cursor = self.db.cursor

            sql = "SELECT Rol FROM usuarios WHERE Nombre = ? AND Contraseña = ?"
            print(f"SQL Query: {sql}")
            print(f"Parameters: usuario={usuario}, password={password}")

            cursor.execute(sql, (usuario, password))
            resultado = cursor.fetchone()

            if resultado:
                return resultado[0]  # Devuelve el rol del usuario
            else:
                return None

        except Exception as e:
            print(f"Error al validar credenciales: {e}")
            return False
        
    def cerrarConexion(self):
        if self.conexion:
            try:
                self.db.conexion.commit()
                self.db.conexion.close()
                print("Conexión cerrada correctamente.")
            except Exception as e:
                print(f"Error al cerrar la conexión: {e}")
