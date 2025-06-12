from .Conexion import ConexionDB
import sqlite3, os

def listarHistoria(CI):
    conexion = ConexionDB()
    sql = """
        SELECT NumeroHistoria, CI, Tratamiento, Fechahistoria, Odontologo
        FROM HistoriaClinica
        WHERE CI = ?
    """
    try:
        conexion.cursor.execute(sql, (CI,))
        return conexion.cursor.fetchall()
    finally:
        conexion.cerrarConexion()


def guardarHistoria(CI, NumeroHistoria, Tratamiento, FechaHistoria, Odontologo):
    conexion = ConexionDB()
    
    # Verificar si el número de historia ya existe para otro paciente
    if verificar_numero_historia_existe(NumeroHistoria, CI):
        raise Exception(f"El número de historia {NumeroHistoria} ya está asignado a otro paciente.")
    
    sql = """
        INSERT INTO HistoriaClinica (CI, NumeroHistoria, Tratamiento, Fechahistoria, Odontologo)
        VALUES (?, ?, ?, ?, ?)
    """
    try:
        conexion.cursor.execute(sql, (CI, NumeroHistoria, Tratamiento, FechaHistoria, Odontologo))
        conexion.conexion.commit()
    finally:
        conexion.cerrarConexion()

def actualizarHistoria(NumeroHistoria, CI, Tratamiento, FechaHistoria, Odontologo):
    conexion = ConexionDB()
    sql = """
        UPDATE HistoriaClinica
        SET Tratamiento = ?, Fechahistoria = ?, Odontologo = ?
        WHERE NumeroHistoria = ? AND CI = ?
    """
    try:
        conexion.cursor.execute(sql, (Tratamiento, FechaHistoria, Odontologo, NumeroHistoria, CI))
        conexion.conexion.commit()
    finally:
        conexion.cerrarConexion()

def eliminarHistoria(NumeroHistoria, CI):
    from .Conexion import ConexionDB
    from tkinter import messagebox

    conexion = ConexionDB()
    sql = "DELETE FROM HistoriaClinica WHERE NumeroHistoria = ? AND CI = ?"
    try:
        conexion.cursor.execute(sql, (NumeroHistoria, CI))
        conexion.conexion.commit()
    except Exception as e:
        messagebox.showerror("Eliminar Historia", f"Error al eliminar historia: {e}")
    finally:
        conexion.cerrarConexion()


def verificar_numero_historia_existe(numero_historia, ci_actual=None):
    """
    Verifica si un número de historia ya existe para otro paciente.
    Si ci_actual se proporciona, excluye ese paciente de la verificación.
    """
    conexion = ConexionDB()
    try:
        if ci_actual:
            sql = """
                SELECT COUNT(*) FROM HistoriaClinica 
                WHERE NumeroHistoria = ? AND CI != ?
            """
            conexion.cursor.execute(sql, (numero_historia, ci_actual))
        else:
            sql = """
                SELECT COUNT(*) FROM HistoriaClinica 
                WHERE NumeroHistoria = ?
            """
            conexion.cursor.execute(sql, (numero_historia,))
        
        resultado = conexion.cursor.fetchone()
        return resultado[0] > 0
    finally:
        conexion.cerrarConexion()


def obtener_numero_historia_paciente(CI):
    """
    Obtiene el número de historia asignado a un paciente específico.
    Retorna None si el paciente no tiene historias.
    """
    conexion = ConexionDB()
    try:
        sql = """
            SELECT DISTINCT NumeroHistoria 
            FROM HistoriaClinica 
            WHERE CI = ? 
            LIMIT 1
        """
        conexion.cursor.execute(sql, (CI,))
        resultado = conexion.cursor.fetchone()
        return resultado[0] if resultado else None
    finally:
        conexion.cerrarConexion()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, '..', 'Database', 'DBhistorias.db')

def guardar_imagen_historia(ci, fecha, ruta_imagen):
    """
    Actualiza el registro de HistoriaClinica para CI+fecha dados,
    guardando la imagen como BLOB en la base de datos.
    """
    conexion = ConexionDB()
    try:
        # Leer la imagen como BLOB
        with open(ruta_imagen, 'rb') as f:
            imagen_blob = f.read()
        
        # Actualizar el registro con la imagen y la ruta
        sql = """
            UPDATE HistoriaClinica
            SET Imagen = ?, RutaImagen = ?
            WHERE CI = ? AND Fechahistoria = ?
        """
        conexion.cursor.execute(sql, (sqlite3.Binary(imagen_blob), ruta_imagen, ci, fecha))
        conexion.conexion.commit()
        
        # Verificar que se actualizó correctamente
        if conexion.cursor.rowcount == 0:
            raise Exception(f"No se encontró historia para CI: {ci} y fecha: {fecha}")
        
        print(f"✓ Imagen guardada correctamente para CI: {ci}, fecha: {fecha}")
        
    except Exception as e:
        print(f"Error al guardar imagen: {e}")
        raise e
    finally:
        conexion.cerrarConexion()

def obtener_imagen_historia(ci, fecha):
    """
    Obtiene los datos BLOB de la imagen asociada a una historia clínica específica.
    Primero intenta usar la ruta guardada, si no existe recupera el BLOB.
    """
    conexion = ConexionDB()
    try:
        # Primero intentar obtener la ruta y la imagen
        sql = """
            SELECT RutaImagen, Imagen
            FROM HistoriaClinica 
            WHERE CI = ? AND Fechahistoria = ?
        """
        conexion.cursor.execute(sql, (ci, fecha))
        resultado = conexion.cursor.fetchone()
        
        if not resultado:
            print(f"No se encontró imagen para CI: {ci}, fecha: {fecha}")
            return None
            
        ruta_imagen, imagen_blob = resultado
        
        # Si la ruta existe y el archivo existe, retornar la ruta
        if ruta_imagen and os.path.exists(ruta_imagen):
            print(f"✓ Usando imagen existente en: {ruta_imagen}")
            return ruta_imagen
            
        # Si no hay ruta o el archivo no existe, pero hay blob
        if imagen_blob:
            print(f"Recuperando imagen desde BLOB para CI: {ci}, fecha: {fecha}")
            
            # Crear directorio temporal si no existe
            temp_dir = os.path.join('imagenes', 'temp')
            os.makedirs(temp_dir, exist_ok=True)
            
            # Generar nombre único para el archivo temporal
            temp_file = os.path.join(temp_dir, f"{ci}_{fecha.replace('-','')}_temp.jpg")
            
            # Guardar BLOB en archivo temporal
            with open(temp_file, 'wb') as f:
                f.write(imagen_blob)
                
            # Actualizar la ruta en la base de datos
            sql_update = """
                UPDATE HistoriaClinica
                SET RutaImagen = ?
                WHERE CI = ? AND Fechahistoria = ?
            """
            conexion.cursor.execute(sql_update, (temp_file, ci, fecha))
            conexion.conexion.commit()
            
            print(f"✓ Imagen guardada en: {temp_file}")
            return temp_file
            
        print(f"No hay imagen ni BLOB para CI: {ci}, fecha: {fecha}")
        return None
        
    except Exception as e:
        print(f"Error al obtener imagen: {e}")
        return None
    finally:
        conexion.cerrarConexion()

def listar_imagenes_paciente(ci):
    """
    Lista todas las imágenes de un paciente específico
    """
    conexion = ConexionDB()
    try:
        sql = """
            SELECT Fechahistoria, Imagen, Tratamiento
            FROM HistoriaClinica 
            WHERE CI = ? AND Imagen IS NOT NULL
            ORDER BY Fechahistoria DESC
        """
        conexion.cursor.execute(sql, (ci,))
        return conexion.cursor.fetchall()
    except Exception as e:
        print(f"Error al listar imágenes: {e}")
        return []
    finally:
        conexion.cerrarConexion()
