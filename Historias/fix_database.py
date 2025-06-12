import sqlite3
import os

# Ruta a la base de datos
db_path = os.path.join('Database', 'DBhistorias.db')

try:
    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Verificar estructura actual de la tabla
    cursor.execute("PRAGMA table_info(HistoriaClinica)")
    columns = cursor.fetchall()
    print("Columnas actuales en HistoriaClinica:")
    for col in columns:
        print(f"  {col[1]} - {col[2]}")
    
    # Verificar si las columnas existen
    column_names = [col[1] for col in columns]
    
    if 'Imagen' not in column_names:
        print("Agregando columna Imagen...")
        cursor.execute("ALTER TABLE HistoriaClinica ADD COLUMN Imagen BLOB")
        conn.commit()
        print("Columna Imagen agregada.")
    else:
        print("Columna Imagen ya existe.")
    
    if 'RutaImagen' not in column_names:
        print("Agregando columna RutaImagen...")
        cursor.execute("ALTER TABLE HistoriaClinica ADD COLUMN RutaImagen TEXT")
        conn.commit()
        print("Columna RutaImagen agregada.")
    else:
        print("Columna RutaImagen ya existe.")
    
    # Verificar estructura final
    cursor.execute("PRAGMA table_info(HistoriaClinica)")
    columns = cursor.fetchall()
    print("\nEstructura final de HistoriaClinica:")
    for col in columns:
        print(f"  {col[1]} - {col[2]}")
    
    conn.close()
    print("\nBase de datos actualizada correctamente.")
    
except Exception as e:
    print(f"Error al actualizar la base de datos: {e}")
