from .Conexion import ConexionDB

def listarHistoria(CI):
    conexion = ConexionDB()
    sql = """
        SELECT idHistoriaClinica, CI, Tratamiento, FechaHistoria, Odontologo
        FROM HistoriaClinica
        WHERE CI = ?
    """
    try:
        conexion.cursor.execute(sql, (CI,))
        return conexion.cursor.fetchall()
    finally:
        conexion.cerrarConexion()


def guardarHistoria(CI, Tratamiento, FechaHistoria, Odontologo):
    conexion = ConexionDB()
    sql = """
        INSERT INTO HistoriaClinica (CI, Tratamiento, FechaHistoria, Odontologo)
        VALUES (?, ?, ?, ?)
    """
    try:
        conexion.cursor.execute(sql, (CI, Tratamiento, FechaHistoria, Odontologo))
        conexion.conexion.commit()
    finally:
        conexion.cerrarConexion()

def actualizarHistoria(idHistoriaClinica, Tratamiento, FechaHistoria, Odontologo):
    conexion = ConexionDB()
    sql = """
        UPDATE HistoriaClinica
        SET Tratamiento = ?, FechaHistoria = ?, Odontologo = ?
        WHERE idHistoriaClinica = ?
    """
    try:
        conexion.cursor.execute(sql, (Tratamiento, FechaHistoria, Odontologo, idHistoriaClinica))
        conexion.conexion.commit()
    finally:
        conexion.cerrarConexion()

def eliminarHistoria(idHistoriaClinica):
    from .Conexion import ConexionDB
    from tkinter import messagebox

    conexion = ConexionDB()
    sql = "DELETE FROM HistoriaClinica WHERE idHistoriaClinica = ?"
    try:
        conexion.cursor.execute(sql, (idHistoriaClinica,))
        conexion.conexion.commit()
    except Exception as e:
        messagebox.showerror("Eliminar Historia", f"Error al eliminar historia: {e}")
    finally:
        conexion.cerrarConexion()

