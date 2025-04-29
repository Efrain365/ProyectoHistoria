import sqlite3

class ConexionDB:
    def __init__(self):
        self.BaseDatos = 'Database/DBhistorias.db'
        self.conexion = sqlite3.connect(self.BaseDatos)
        self.cursor = self.conexion.cursor()

    def cerrarConexion(self):
        self.conexion.commit()
        self.conexion.close()
