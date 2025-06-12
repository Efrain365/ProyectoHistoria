from .Conexion import ConexionDB

def obtenerPlanTratamiento(CI):
    """
    Devuelve una tupla (R1, R2, R3, R4, Limpieza, Extraccion, Otros)
    o None si no existe aún.
    """
    conexion = ConexionDB()
    sql = """
      SELECT R1, R2, R3, R4, Limpieza, Extraccion, Otros, Nota
      FROM PlanDeTratamiento
      WHERE CI = ?
    """
    try:
        conexion.cursor.execute(sql, (CI,))
        return conexion.cursor.fetchone()
    finally:
        conexion.cerrarConexion()

def guardarPlanTratamiento(ci, datos_plan):
    """
    Guarda o actualiza un plan de tratamiento en la base de datos.
    - Si el plan ya existe, lo actualiza.
    - Si no existe, lo crea.
    """
    conexion = ConexionDB()
    try:
        sql_verificar = "SELECT 1 FROM PlanDeTratamiento WHERE CI = ?"
        conexion.cursor.execute(sql_verificar, (ci,))
        existe = conexion.cursor.fetchone()

        if existe:
            sql_actualizar = """
                UPDATE PlanDeTratamiento
                SET R1 = ?, R2 = ?, R3 = ?, R4 = ?, Limpieza = ?, Extraccion = ?, Otros = ?, Nota = ?
                WHERE CI = ?
            """
            conexion.cursor.execute(sql_actualizar, (*datos_plan.values(), ci))
        else:
            sql_insertar = """
                INSERT INTO PlanDeTratamiento (CI, R1, R2, R3, R4, Limpieza, Extraccion, Otros, Nota)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            conexion.cursor.execute(sql_insertar, (ci, *datos_plan.values()))
        conexion.conexion.commit()
    finally:
        conexion.cerrarConexion()

def eliminarPlanTratamiento(ci):
    conexion = ConexionDB()
    try:
        sql = "DELETE FROM PlanDeTratamiento WHERE CI = ?"
        conexion.cursor.execute(sql, (ci,))
        conexion.conexion.commit()
    finally:
        conexion.cerrarConexion()
