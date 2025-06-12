from .Conexion import ConexionDB
from tkinter import messagebox 
from fpdf import FPDF
from PIL import Image, ImageTk
from tkinter.filedialog import asksaveasfilename
import sqlite3
import os
from .historiaClinicaDao import listar_imagenes_paciente
import os
from .historiaClinicaDao import listar_imagenes_paciente

def guardarDatoPaciente(persona):
    conexion = ConexionDB()
    sql = """INSERT INTO Persona (Nombre, CI, Edad, Tlfn, Alergia, Enfermedad, Medicamento) 
    VALUES (?, ?, ?, ?, ?, ?, ?)"""
    valores = (persona.Nombre, persona.CI, persona.Edad, persona.Tlfn, persona.Alergia, persona.Enfermedad, persona.Medicamento)

    try:
        conexion.cursor.execute(sql, valores)
        conexion.conexion.commit()  
        Title = 'Registrar Paciente'
        Mensaje = 'Paciente Registrado Exitosamente'
        messagebox.showinfo(Title, Mensaje)
    except sqlite3.Error as e:
        Title = 'Registrar Paciente'
        Mensaje = f'Error al Registrar Paciente: {e}'
        messagebox.showerror(Title, Mensaje)
    finally:
        conexion.cerrarConexion()

def listar():
    conexion = ConexionDB()
    listaPersona = []
    sql = 'SELECT * FROM Persona'

    try: 
        conexion.cursor.execute(sql)
        listaPersona = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except:
        title = 'Datos'
        mensaje = 'Registros no existen'
        messagebox.showwarning(title, mensaje)
    return listaPersona 

def listarCondicion(where):
    conexion = ConexionDB()
    listapersona = []
    sql = f'SELECT * FROM Persona {where}'

    try: 
        conexion.cursor.execute(sql)
        listapersona = conexion.cursor.fetchall()
        conexion.cerrarConexion()
    except:
        title = 'Datos'
        mensaje = 'Registros no existen'
        messagebox.showwarning(title, mensaje)
    return listapersona

def eliminarPaciente(CI):
    conexion = ConexionDB()
    sql = """DELETE FROM Persona WHERE CI = ?"""

    try:
        conexion.cursor.execute(sql, (CI,))
        conexion.conexion.commit()
        title = 'Eliminar Paciente'
        mensaje = 'Paciente eliminado exitosamente.'
        messagebox.showinfo(title, mensaje)
    except Exception as e:
        title = 'Eliminar Paciente'
        mensaje = f'Error al eliminar paciente: {e}'
        messagebox.showerror(title, mensaje)
    finally:
        conexion.cerrarConexion()

class Persona:
    def __init__(self, Nombre, CI, Edad, Tlfn, Alergia, Enfermedad, Medicamento):
        self.Nombre = Nombre
        self.CI = CI
        self.Edad = Edad
        self.Tlfn = Tlfn
        self.Alergia = Alergia
        self.Enfermedad = Enfermedad
        self.Medicamento = Medicamento
    
    def __str__(self):
        return f'Persona[{self.Nombre}, {self.CI}, {self.Edad}, {self.Tlfn}, {self.Alergia}, {self.Enfermedad}, {self.Medicamento}]'
    
def actualizarPaciente(CI_original, persona):
    from .Conexion import ConexionDB
    conexion = ConexionDB()
    cursor = conexion.cursor
    
    try:
        cursor.execute("""
            UPDATE Persona SET
                Nombre = ?, 
                Edad = ?, 
                Tlfn = ?, 
                Enfermedad = ?, 
                Alergia = ?, 
                Medicamento = ?, 
                CI = ?
            WHERE CI = ?
        """, (persona.Nombre, persona.Edad, persona.Tlfn,
            persona.Enfermedad, persona.Alergia, persona.Medicamento,
            persona.CI, CI_original))

        conexion.conexion.commit()
        messagebox.showinfo("Actualizar Paciente", "Paciente actualizado exitosamente")

    except sqlite3.IntegrityError:
        messagebox.showerror("Actualizar Paciente", "La cédula ingresada ya está registrada.")

    except Exception as e:
        messagebox.showerror("Actualizar Paciente", f"Error inesperado: {e}")

    finally:
        conexion.cerrarConexion()

def guardar_pdf(pdf, nombre_default):
    ruta_pdf = asksaveasfilename(
        title="Guardar PDF",
        defaultextension=".pdf",
        filetypes=[("Archivos PDF", "*.pdf")],
        initialfile=nombre_default
    )
    if ruta_pdf:  # Si el usuario selecciona una ruta
        pdf.output(ruta_pdf)
        return ruta_pdf
    else:
        return None

def Imprimir(CI):
    try:
        # Crear instancia de conexión
        conexion = ConexionDB()

        # Obtener datos del paciente
        sql_paciente = """
            SELECT Nombre, Edad, CI, Tlfn, Alergia, Enfermedad, Medicamento 
            FROM Persona 
            WHERE CI = ?
        """
        conexion.cursor.execute(sql_paciente, (CI,))
        paciente = conexion.cursor.fetchone()

        if not paciente:
            raise ValueError(f"No se encontró el paciente con la cédula {CI}.")

        # Obtener tratamientos
        sql_tratamientos = """
            SELECT FechaHistoria, Tratamiento, Odontologo
            FROM HistoriaClinica
            WHERE CI = ?
        """
        conexion.cursor.execute(sql_tratamientos, (CI,))
        tratamientos = conexion.cursor.fetchall()

        # Crear el PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Logo
        pdf.image(r"C:\Users\Efrain\Desktop\CARPETA GLOWADENT\Horizontal-Transparente-1.png", x=10, y=10, w=88, h=20)

        # Título (posicionado arriba y a la derecha, sobre la tabla)
        pdf.set_xy(130, 40)
        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(0, 10, txt="HISTORIA CLÍNICA", ln=True, align="L")
        pdf.ln(10)


        # Posicionar la información básica del paciente
        pdf.set_xy(10, 50)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(90, 10, txt=(
            f"Nombre: {paciente[0]}\n"
            f"Edad: {paciente[1]} años\n"
            f"Teléfono: {paciente[3]}\n"
            f"Cédula: {paciente[2]}\n"
            f"Alergia: {paciente[4]}\n"
            f"Enfermedades: {paciente[5]}\n"
            f"Medicamentos: {paciente[6]}"
        ))

        # Posicionar la tabla de tratamientos al lado derecho
        pdf.set_xy(100, 50)
        pdf.set_font("Arial", style="B", size=10)
        pdf.cell(20, 10, txt="Fecha", border=1, align="C")
        pdf.cell(60, 10, txt="Tratamiento", border=1, align="C")
        pdf.cell(20, 10, txt="Dr(a)", border=1, align="C")
        pdf.ln()

        pdf.set_font("Arial", size=10)
        for tratamiento in tratamientos:
            pdf.set_x(100)
            pdf.cell(20, 10, txt=tratamiento[0], border=1, align="C")
            pdf.cell(60, 10, txt=tratamiento[1], border=1, align="C")
            pdf.cell(20, 10, txt=tratamiento[2], border=1, align="C")
            pdf.ln()

        # Sección de Imágenes Radiografías
        pdf.add_page()
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(0, 10, txt="IMÁGENES RADIOGRAFÍAS", ln=True, align="C")
        pdf.ln(10)

        # Obtener y mostrar las imágenes del paciente
        imagenes = listar_imagenes_paciente(CI)
        if imagenes:
            y_pos = pdf.get_y()
            for fecha, imagen_blob, tratamiento in imagenes:
                if imagen_blob:
                    # Crear un archivo temporal para la imagen
                    temp_dir = os.path.join('imagenes', 'temp')
                    os.makedirs(temp_dir, exist_ok=True)
                    temp_file = os.path.join(temp_dir, f"{CI}_{fecha.replace('-','_')}_temp.jpg")
                    
                    # Guardar el BLOB en un archivo temporal
                    with open(temp_file, 'wb') as f:
                        f.write(imagen_blob)
                    
                    # Agregar la imagen al PDF
                    try:
                        # Calcular dimensiones para la imagen (máximo 180 de ancho)
                        img_width = 180
                        img_height = 120  # Altura proporcional
                        
                        # Si no hay espacio suficiente en la página actual, agregar nueva página
                        if y_pos + img_height + 20 > pdf.h:
                            pdf.add_page()
                            y_pos = pdf.get_y()
                        
                        # Agregar la imagen
                        pdf.image(temp_file, x=(210-img_width)/2, y=y_pos, w=img_width, h=img_height)
                        
                        # Agregar fecha y tratamiento debajo de la imagen
                        y_pos += img_height + 5
                        pdf.set_y(y_pos)
                        pdf.set_font("Arial", size=10)
                        pdf.cell(0, 10, f"Fecha: {fecha} - {tratamiento}", ln=True, align="C")
                        y_pos = pdf.get_y() + 10
                        
                        # Eliminar el archivo temporal
                        os.remove(temp_file)
                    except Exception as e:
                        print(f"Error al procesar imagen: {e}")
        else:
            pdf.cell(0, 10, txt="No hay imágenes registradas", ln=True, align="C")

        # Guardar el PDF
        nombre_default = f"Historia_Clinica_{CI}.pdf"
        ruta_pdf = guardar_pdf(pdf, nombre_default)
        if ruta_pdf:
            print(f"PDF generado correctamente")
            return ruta_pdf  # Devuelve la ruta si se guardó
        else:
            print("Guardado cancelado por el usuario.")
            return None  # Devuelve None si el usuario canceló

    except Exception as e:
        raise ValueError(f"Error al generar el PDF: {e}")
    finally:
        # Cerrar conexión
        conexion.cerrarConexion()


class Buscarpacientes:
    def buscar_por_cedula(self, cedula):
        """
        Busca pacientes por cédula en la tabla Persona.
        Devuelve una lista de tuplas en el orden:
        (CI, Nombre, Edad, Tlfn, Alergia, Enfermedad, Medicamento)
        """
        conexion = ConexionDB()
        cursor   = conexion.cursor
        try:
            sql = """
                SELECT Nombre, CI, Edad, Tlfn, Alergia, Enfermedad, Medicamento
                FROM Persona
                WHERE CI = ?
            """
            cursor.execute(sql, (cedula,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al buscar por cédula: {e}")
            return []
        finally:
            conexion.cerrarConexion()

    def buscar_por_fecha(self, fecha):
        """
        Busca pacientes que tienen historia en la fecha dada.
        Hace JOIN con HistoriaClinica y devuelve tuplas en el mismo orden:
        (CI, Nombre, Edad, Tlfn, Alergia, Enfermedad, Medicamento)
        """
        conexion = ConexionDB()
        cursor   = conexion.cursor
        try:
            sql = """
                SELECT DISTINCT 
                    P.Nombre, P.CI, P.Edad, P.Tlfn, 
                    P.Alergia, P.Enfermedad, P.Medicamento
                FROM Persona P
                JOIN HistoriaClinica H ON P.CI = H.CI
                WHERE H.FechaHistoria = ?
            """
            cursor.execute(sql, (fecha,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al buscar por fecha: {e}")
            return []
        finally:
            conexion.cerrarConexion()

    def buscar_por_rango_fechas(self, fecha_desde, fecha_hasta):
        """
        Busca pacientes que tienen historia clínica en un rango de fechas.
        Hace JOIN con HistoriaClinica y devuelve tuplas en el mismo orden:
        (Nombre, CI, Edad, Tlfn, Alergia, Enfermedad, Medicamento)
        """
        conexion = ConexionDB()
        cursor   = conexion.cursor
        try:
            # Convertir fechas de DD-MM-YYYY a YYYY-MM-DD para comparación en SQLite
            import datetime
            fecha_desde_obj = datetime.datetime.strptime(fecha_desde, '%d-%m-%Y')
            fecha_hasta_obj = datetime.datetime.strptime(fecha_hasta, '%d-%m-%Y')
            
            fecha_desde_sql = fecha_desde_obj.strftime('%Y-%m-%d')
            fecha_hasta_sql = fecha_hasta_obj.strftime('%Y-%m-%d')
            
            sql = """
                SELECT DISTINCT 
                    P.Nombre, P.CI, P.Edad, P.Tlfn, 
                    P.Alergia, P.Enfermedad, P.Medicamento
                FROM Persona P
                JOIN HistoriaClinica H ON P.CI = H.CI
                WHERE date(substr(H.FechaHistoria, 7, 4) || '-' || 
                          substr(H.FechaHistoria, 4, 2) || '-' || 
                          substr(H.FechaHistoria, 1, 2)) 
                      BETWEEN ? AND ?
            """
            cursor.execute(sql, (fecha_desde_sql, fecha_hasta_sql))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al buscar por rango de fechas: {e}")
            return []
        finally:
            conexion.cerrarConexion()
