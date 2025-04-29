from .Conexion import ConexionDB
from tkinter import messagebox 
import sqlite3

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

