import sqlite3
import os

def agregar_columna_imagen():
    """Agrega la columna Imagen a la tabla HistoriaClinica si no existe"""
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, 'Database', 'DBhistorias.db')
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        
        # Verificar si la columna Imagen ya existe
        cur.execute("PRAGMA table_info(HistoriaClinica)")
        columns = cur.fetchall()
        column_names = [col[1] for col in columns]
        
        print("Columnas actuales en HistoriaClinica:")
        for name in column_names:
            print(f"  - {name}")
        
        if 'Imagen' not in column_names:
            print("\nAgregando columna 'Imagen'...")
            cur.execute("ALTER TABLE HistoriaClinica ADD COLUMN Imagen BLOB")
            conn.commit()
            print("✓ Columna 'Imagen' agregada exitosamente")
        else:
            print("\n✓ La columna 'Imagen' ya existe")
        
        # Verificar estructura final
        cur.execute("PRAGMA table_info(HistoriaClinica)")
        columns = cur.fetchall()
        print("\nEstructura final de la tabla:")
        for col in columns:
            print(f"  {col[1]} - {col[2]}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    agregar_columna_imagen()
