import sqlite3
import os

class ConexionDB:
    def __init__(self):
        try:
            # Detectar la ubicación del archivo actual
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            
            # Construir la ruta a la base de datos
            self.BaseDatos = os.path.join(BASE_DIR, '..', 'Database', 'DBhistorias.db')
            
            # Conectar a la base de datos
            self.conexion = sqlite3.connect(self.BaseDatos)
            self.cursor = self.conexion.cursor()
        except sqlite3.Error as e:
            raise sqlite3.OperationalError(f"Error al conectar con la base de datos: {e}")

    def cerrarConexion(self):
        try:
            self.conexion.commit()
            self.conexion.close()
        except sqlite3.Error as e:
            raise sqlite3.OperationalError(f"Error al cerrar la conexión: {e}")
