import shutil
import tkinter as tk
from tkinter import *
from tkinter import ttk, Toplevel
from tkinter import messagebox
from Modelo.planTratamientoDao import guardarPlanTratamiento, obtenerPlanTratamiento
from Modelo.PacienteDao import Persona, listarCondicion, listar, eliminarPaciente, Imprimir, Buscarpacientes
from Modelo.historiaClinicaDao import (listarHistoria, guardar_imagen_historia, 
                                     obtener_imagen_historia, listar_imagenes_paciente)
#from paciente.gui import Frame

from tkinter import filedialog
from tkcalendar import DateEntry
import sqlite3
import sys
import datetime, os
from PIL import Image, ImageTk

class Frame(tk.Frame):
    def __init__(self, root, rol):
        super().__init__(root, width=1280, height=720)
        self.CI_original = None
        self.historia_original = None       
        self.root = root
        self.rol = rol # Guardar el rol del usuario
        self.pack()
        self.config(bg='papaya whip')
        self.campospaciente()
        self.deshabilitar()
        self.tablaPaciente()
        self.root.protocol("WM_DELETE_WINDOW", self.confirmar_cierre)
        self.centrarVentana(root, 1280, 585)
        self.dao = Buscarpacientes()
        self.root.title("REGISTRAR PACIENTES")
        # Agregar atributo para mantener referencia de la imagen actual
        self.current_image = None

 #LABELS

    def validar_solo_numeros(self, char):
        return char.isdigit() or char == ""

    def validar_solo_letras(self, char):
        return char.isalpha() or char.isspace() or char == ""

    def campospaciente(self):
        # Registrar las funciones de validación
        validar_numeros = (self.register(self.validar_solo_numeros), '%S')
        validar_letras = (self.register(self.validar_solo_letras), '%S')

        self.lblNombre = tk.Label(self, text= 'Nombre: ')
        self.lblNombre.config(font=('APTOS DISPLAY',14), bg='papaya whip')
        self.lblNombre.grid(column=0, row=0, padx=10, pady= 5, sticky= E)

        self.lblCI = tk.Label(self, text= 'Cedula: ')
        self.lblCI.config(font=('APTOS DISPLAY',14), bg='papaya whip')
        self.lblCI.grid(column=0, row=1, padx=10, pady= 5, sticky= E)

        self.lblEdad = tk.Label(self, text= 'Edad: ')
        self.lblEdad.config(font=('APTOS DISPLAY',14), bg='papaya whip')
        self.lblEdad.grid(column=0, row=2, padx=10, pady= 5, sticky= E)

        self.lblTlfn = tk.Label(self, text= 'Telefono: ')
        self.lblTlfn.config(font=('APTOS DISPLAY',14), bg='papaya whip')
        self.lblTlfn.grid(column=0, row=3, padx=10, pady= 5, sticky= E)

        self.lblAlergia = tk.Label(self, text= 'Alergia: ')
        self.lblAlergia.config(font=('APTOS DISPLAY',14), bg='papaya whip')
        self.lblAlergia.grid(column=0, row=4, padx=10, pady= 5, sticky= E)

        self.lblEnfermedad = tk.Label(self, text= 'Enfermedad: ')
        self.lblEnfermedad.config(font=('APTOS DISPLAY',14), bg='papaya whip')
        self.lblEnfermedad.grid(column=0, row=5, padx=10, pady= 5, sticky= E)

        self.lblMedicamento = tk.Label(self, text= 'Medicamento: ')
        self.lblMedicamento.config(font=('APTOS DISPLAY',14), bg='papaya whip')
        self.lblMedicamento.grid(column=0, row=6, padx=10, pady= 5, sticky= E)

        #ENTRYS

        self.svNombre = tk.StringVar()
        self.entryNombre = tk.Entry(self, textvariable=self.svNombre)
        self.entryNombre.config(width=50, font=('APTOS DISPLAY',14), validate='key', validatecommand=validar_letras)
        self.entryNombre.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

        self.svCI = tk.StringVar()
        self.entryCI = tk.Entry(self, textvariable=self.svCI)
        self.entryCI.config(width=50, font=('APTOS DISPLAY',14), validate='key', validatecommand=validar_numeros)
        self.entryCI.grid(column=1, row=1, padx=10, pady=5, columnspan=2)

        self.svEdad = tk.StringVar()
        self.entryEdad = tk.Entry(self, textvariable=self.svEdad)
        self.entryEdad.config(width=50, font=('APTOS DISPLAY',14), validate='key', validatecommand=validar_numeros)
        self.entryEdad.grid(column=1, row=2, padx=10, pady=5, columnspan=2)

        self.svTlfn = tk.StringVar()
        self.entryTlfn = tk.Entry(self, textvariable=self.svTlfn)
        self.entryTlfn.config(width=50, font=('APTOS DISPLAY',14), validate='key', validatecommand=validar_numeros)
        self.entryTlfn.grid(column=1, row=3, padx=10, pady=5, columnspan=2)

        self.svAlergia = tk.StringVar()
        self.entryAlergia = tk.Entry(self, textvariable=self.svAlergia)
        self.entryAlergia.config(width=50, font=('APTOS DISPLAY',14), validate='key', validatecommand=validar_letras)
        self.entryAlergia.grid(column=1, row=4, padx=10, pady=5, columnspan=2)

        self.svEnfermedad = tk.StringVar()
        self.entryEnfermedad = tk.Entry(self, textvariable=self.svEnfermedad)
        self.entryEnfermedad.config(width=50, font=('APTOS DISPLAY',14), validate='key', validatecommand=validar_letras)
        self.entryEnfermedad.grid(column=1, row=5, padx=10, pady=5, columnspan=2)

        self.svMedicamento = tk.StringVar()
        self.entryMedicamento = tk.Entry(self, textvariable=self.svMedicamento)
        self.entryMedicamento.config(width=50, font=('APTOS DISPLAY',14), validate='key', validatecommand=validar_letras)
        self.entryMedicamento.grid(column=1, row=6, padx=10, pady=5, columnspan=2)

        #BUSCADOR

        #LABEL BUSCADOR
        self.lblBuscarCI = tk.Label(self, text='Buscar por CI: ')
        self.lblBuscarCI.config(font=('APTOS DISPLAY',14), bg='papaya whip')
        self.lblBuscarCI.grid(column=3, row=0, padx=(50,10), pady=5, sticky=E)

        #ENTRY BUSCADOR CI
        self.svBuscarCI = tk.StringVar()
        self.entryBuscarCI = tk.Entry(self, textvariable=self.svBuscarCI)
        self.entryBuscarCI.config(width=20, font=('APTOS DISPLAY',14))
        self.entryBuscarCI.grid(column=4, row=0, padx=10, pady=5, columnspan=2, sticky=W)

        # Label Buscar por fecha (centrado)
        self.lblBuscarFecha = tk.Label(self, text='Buscar por fecha')
        self.lblBuscarFecha.config(font=('APTOS DISPLAY',14), bg='papaya whip')
        self.lblBuscarFecha.grid(column=3, row=1, columnspan=3, pady=(10,5))

        # Frame para contener los campos de fecha
        self.frameFechas = tk.Frame(self, bg='papaya whip')
        self.frameFechas.grid(column=3, row=2, columnspan=3, padx=10, pady=5)

        # Desde
        self.lblDesde = tk.Label(self.frameFechas, text='Desde:', bg='papaya whip', font=('APTOS DISPLAY',12))
        self.lblDesde.grid(row=0, column=0, padx=5)
        
        self.svFechaDesde = tk.StringVar()
        self.entryFechaDesde = DateEntry(self.frameFechas, textvariable=self.svFechaDesde, 
                                       width=12, font=('APTOS DISPLAY',12),
                                       date_pattern='dd-mm-yyyy',
                                       locale='es_ES')
        self.entryFechaDesde.grid(row=0, column=1, padx=5)

        # Hasta
        self.lblHasta = tk.Label(self.frameFechas, text='Hasta:', bg='papaya whip', font=('APTOS DISPLAY',12))
        self.lblHasta.grid(row=0, column=2, padx=5)
        
        self.svFechaHasta = tk.StringVar()
        self.entryFechaHasta = DateEntry(self.frameFechas, textvariable=self.svFechaHasta, 
                                       width=12, font=('APTOS DISPLAY',12),
                                       date_pattern='dd-mm-yyyy',
                                       locale='es_ES')
        self.entryFechaHasta.grid(row=0, column=3, padx=5)

        #BUTTON BUSCADOR
        self.btnBuscarCondicion = tk.Button(self, text= 'Buscar', command= self.buscar)
        self.btnBuscarCondicion.config(width=20, font=('APTOS DISPLAY',12,'bold'), fg='#DAD5D6', bg="#4580D8", cursor='hand2', activebackground='papaya whip')
        self.btnBuscarCondicion.grid(column=3, row=3, padx=10, pady= 5, columnspan= 1)

        self.btnLimpiarBuscador = tk.Button(self, text= 'Limpiar', command= self.LimpiarBuscador)
        self.btnLimpiarBuscador.config(width=20, font=('APTOS DISPLAY',12,'bold'), fg='#DAD5D6', bg="#2216CC", cursor='hand2', activebackground='papaya whip')
        self.btnLimpiarBuscador.grid(column=4, row=3, padx=10, pady= 5, columnspan= 1)

        #BUTTONS

        self.btnNuevo = tk.Button(self, text= 'Nuevo', command=self.habilitar)
        self.btnNuevo.config(width=20, font=('APTOS DISPLAY',12,'bold'), fg='#DAD5D6', bg="#4580D8", cursor='hand2', activebackground='papaya whip')
        self.btnNuevo.grid(column=0, row=7, padx=10, pady= 5)

        self.btnGuardar = tk.Button(self, text= 'Guardar', command=self.guardarPaciente)
        self.btnGuardar.config(width=20, font=('APTOS DISPLAY',12,'bold'), fg='#DAD5D6', bg="#1DB92A", cursor='hand2', activebackground='papaya whip')
        self.btnGuardar.grid(column=1, row=7, padx=10, pady= 5)

        self.btnCancelar = tk.Button(self, text= 'Cancelar', command=self.deshabilitar)
        self.btnCancelar.config(width=20, font=('APTOS DISPLAY',12,'bold'), fg='#DAD5D6', bg="#D42727", cursor='hand2', activebackground='papaya whip')
        self.btnCancelar.grid(column=2, row=7, padx=10, pady= 5)

        self.btn_generar_pdf = tk.Button(self, text="Imprimir Historia", command=self.Imprimir_historia)
        self.btn_generar_pdf.config(width=20, font=('APTOS DISPLAY', 12, 'bold'), fg='#DAD5D6', bg="#6B37CC", cursor='hand2', activebackground='papaya whip')
        self.btn_generar_pdf.grid(column=4, row=7, padx=10, pady=5)

        self.btnEditarPaciente = tk.Button(self, text='Editar Paciente', command=self.editarPaciente)
        self.btnEditarPaciente.config(width= 20, font=('APTOS DISPLAY',12,'bold'), fg='#DAD5D6', bg="#472FCF", activebackground='papaya whip', cursor='hand2')
        self.btnEditarPaciente.grid(row=9, column=0, padx=10, pady=5)

        self.btnEliminarPaciente = tk.Button(self, text='Eliminar Paciente', command= self.eliminarDatoPaciente)
        self.btnEliminarPaciente.config(width= 20, font=('APTOS DISPLAY',12,'bold'), fg='#DAD5D6', bg="#CE2929", activebackground='papaya whip', cursor='hand2')
        self.btnEliminarPaciente.grid(row=9, column=1, padx=10, pady=5)

        self.btnHistorialPaciente = tk.Button(self, text='Historial Paciente', command= self.historiaClinica)
        self.btnHistorialPaciente.config(width= 20, font=('APTOS DISPLAY',12,'bold'), fg='#DAD5D6', bg="#30CEAB", activebackground='papaya whip', cursor='hand2')
        self.btnHistorialPaciente.grid(row=9, column=2, padx=10, pady=5) 

        self.btnPlanTratamiento = tk.Button( self, text='Plan de Tratamiento', command= self.abrirPlanTratamiento)
        self.btnPlanTratamiento.config(width=20, font=('APTOS DISPLAY',12,'bold'),fg='#DAD5D6', bg="#C56730",activebackground='papaya whip',cursor='hand2')
        self.btnPlanTratamiento.grid(row=9, column=3, padx=10, pady=5)

        self.btnSalir = tk.Button(self, text='Salir', command= self.cerrarventana)
        self.btnSalir.config(width= 20, font=('APTOS DISPLAY',12,'bold'), fg='#DAD5D6', bg="#161414", activebackground='papaya whip', cursor='hand2')
        self.btnSalir.grid(row=9, column=4, padx=10, pady=5)

        # Deshabilitar o habilitar botones según el rol
        if self.rol == "Usuario":
            self.btnEditarPaciente.config(state="disabled")
            self.btnEliminarPaciente.config(state="disabled")
            
        elif self.rol == "Admin":
            self.btnNuevo.config(state="normal")
            self.btnGuardar.config(state="normal")
            self.btnCancelar.config(state="normal")
            self.btnEditarPaciente.config(state="normal")
            self.btnEliminarPaciente.config(state="normal")
            self.btnBuscarCondicion.config(state="normal")
            self.btnLimpiarBuscador.config(state="normal")
            self.btn_generar_pdf.config(state="normal")
            self.btnHistorialPaciente.config(state="normal")
            self.btnPlanTratamiento.config(state="normal")
            self.btnSalir.config(state="normal")

    def LimpiarBuscador(self):
        self.svFechaDesde.set('')
        self.svFechaHasta.set('')
        self.svBuscarCI.set('')
        self.tablaPaciente()

    def buscar(self):
        cedula = self.entryBuscarCI.get().strip()
        fecha_desde = self.svFechaDesde.get().strip()
        fecha_hasta = self.svFechaHasta.get().strip()

        if not cedula and not fecha_desde and not fecha_hasta:
            messagebox.showerror("Error", "Debe ingresar una cédula o un rango de fechas para buscar.")
            return

        # Inicializamos `resultados` en None
        resultados = None

        # Si hay cédula, validar y buscar por cédula
        if cedula:
            if not cedula.isdigit():
                messagebox.showerror("Error", "La cédula debe contener solo números.")
                return
            resultados = self.dao.buscar_por_cedula(cedula)

        # Si no hay cédula pero sí fechas, validar y buscar por rango de fechas
        elif fecha_desde or fecha_hasta:
            # Validar que ambas fechas estén presentes
            if not fecha_desde or not fecha_hasta:
                messagebox.showerror("Error", "Debe ingresar tanto la fecha 'Desde' como la fecha 'Hasta'.")
                return
            
            # Validar formato de fechas
            if not self.es_fecha_valida(fecha_desde) or not self.es_fecha_valida(fecha_hasta):
                messagebox.showerror("Error", "Las fechas deben estar en formato DD-MM-YYYY.")
                return
            
            # Validar que la fecha desde sea menor o igual a la fecha hasta
            try:
                fecha_desde_obj = datetime.datetime.strptime(fecha_desde, '%d-%m-%Y')
                fecha_hasta_obj = datetime.datetime.strptime(fecha_hasta, '%d-%m-%Y')
                
                if fecha_desde_obj > fecha_hasta_obj:
                    messagebox.showerror("Error", "La fecha 'Desde' debe ser anterior o igual a la fecha 'Hasta'.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Error al validar las fechas.")
                return
            
            resultados = self.dao.buscar_por_rango_fechas(fecha_desde, fecha_hasta)

        # Mostrar resultados
        if resultados:
            self.actualizar_tabla(resultados)
        else:
            messagebox.showinfo("Sin resultados", "No se encontraron pacientes para la búsqueda realizada.")

        
    def actualizar_tabla(self, resultados):
        self.tabla.delete(*self.tabla.get_children())
        for fila in resultados:
            # fila = (Nombre, CI, Edad, Tlfn, Alergia, Enfermedad, Medicamento)
            nombre = fila[0]
            resto  = fila[1:]
            self.tabla.insert('', 'end', text=nombre, values=resto)


        
    def Imprimir_historia(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showerror("Error", "Debe seleccionar un paciente.")
            return

        valores = self.tabla.item(seleccion)["values"]
        if not valores:
            messagebox.showerror("Error", "No se pudieron obtener los datos del paciente.")
            return

        CI = valores[0]  
        try:
            ruta_pdf = Imprimir(CI)  
            if ruta_pdf:  
                messagebox.showinfo("Éxito", f"Historia clínica generada para C.I. {CI} en:\n{ruta_pdf}")
            else:  
                messagebox.showwarning("Cancelado", "El guardado del PDF fue cancelado.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar la historia clínica: {e}")

    def guardarPaciente(self):
        if not self.validar_campos(self.entryNombre, self.entryCI, self.entryEdad, self.entryTlfn, self.entryEnfermedad, self.entryAlergia, self.entryMedicamento):
            messagebox.showerror("Error", "Todos los campos deben ser rellenados")
            return
        
        from Modelo.PacienteDao import guardarDatoPaciente, actualizarPaciente

        nombre     = self.svNombre.get()
        ci         = self.svCI.get()
        edad       = self.svEdad.get()
        telefono   = self.svTlfn.get()
        alergia    = self.svAlergia.get()
        enfermedad = self.svEnfermedad.get()
        medicamento= self.svMedicamento.get()

        persona = Persona(nombre, ci, edad, telefono, alergia, enfermedad, medicamento)

        try:
            if self.CI_original:
                actualizarPaciente(self.CI_original, persona)
                self.CI_original = None
            else:
                guardarDatoPaciente(persona)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")
            return

        self.deshabilitar()
        self.tablaPaciente()

    def habilitar(self):
        self.svNombre.set('')
        self.svCI.set('')
        self.svEdad.set('')
        self.svTlfn.set('')
        self.svAlergia.set('')
        self.svMedicamento.set('')
        self.svEnfermedad.set('')

        self.entryNombre.config(state='normal')
        self.entryCI.config(state='normal')
        self.entryEdad.config(state='normal')
        self.entryTlfn.config(state='normal')
        self.entryAlergia.config(state='normal')
        self.entryEnfermedad.config(state='normal')
        self.entryMedicamento.config(state='normal')
        
        self.btnGuardar.config(state='normal')
        self.btnCancelar.config(state='normal')

    def deshabilitar(self):
        self.svNombre.set('')
        self.svCI.set('')
        self.svEdad.set('')
        self.svTlfn.set('')
        self.svAlergia.set('')
        self.svMedicamento.set('')
        self.svEnfermedad.set('')

        self.entryNombre.config(state='disabled')
        self.entryCI.config(state='disabled')
        self.entryEdad.config(state='disabled')
        self.entryTlfn.config(state='disabled')
        self.entryAlergia.config(state='disabled')
        self.entryEnfermedad.config(state='disabled')
        self.entryMedicamento.config(state='disabled')
        
        self.btnGuardar.config(state='disabled')
        self.btnCancelar.config(state='disabled')
    
    def cerrarventana(self):
        import HistoriaClinica
        if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?"):
            if not HistoriaClinica.is_logging_in:
                self.root.destroy()
                sys.exit()

    def tablaPaciente(self, where=""):
      
        if len(where) > 0:
            self.listaPersona = listarCondicion(where)
        else:
            self.listaPersona = listar()
            #self.listaPersona.reverse()

        if not self.listaPersona:
            self.listaPersona = []

        self.tabla = ttk.Treeview(self, columns=('Nombre','CI', 'Edad','Tlfn','Alergia','Enfermedad','Medicamento'))
        self.tabla.grid(column=0, row= 8, columnspan=7, sticky='nse')

        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.tabla.yview)
        self.scroll.grid(row=8, column=8, sticky='nse')

        self.tabla.configure(yscrollcommand=self.scroll.set)
        

        self.tabla.tag_configure('evenrow', background='#C5EAFE')

        # Ocultar la columna #7
        self.tabla.column("#7", width=0, stretch=NO)
        self.tabla.heading("#7", text="")
        
        self.tabla.heading('#0', text='Nombre')
        self.tabla.heading('#1', text='CI')
        self.tabla.heading('#2', text='Edad')
        self.tabla.heading('#3', text='Tlfn')
        self.tabla.heading('#4', text='Alergia')
        self.tabla.heading('#5', text='Enfermedad')
        self.tabla.heading('#6', text='Medicamento')

        self.tabla.column("#0", anchor=W, width=350)
        self.tabla.column("#1", anchor=W, width=120)
        self.tabla.column("#2", anchor=W, width=100)
        self.tabla.column("#3", anchor=W, width=120)
        self.tabla.column("#4", anchor=W, width=192)
        self.tabla.column("#5", anchor=W, width=192)
        self.tabla.column("#6", anchor=W, width=192)

        for p in self.listaPersona:

            self.tabla.insert('',0,text=p[1], values=(p[0],p[3],p[4],p[2],p[5],p[6]), tags=('evenrow',))

        #BUTTONS

        self.btnNuevo = tk.Button(self, text= 'Nuevo', command=self.habilitar)
        self.btnNuevo.config(width=20, font=('APTOS DISPLAY',12,'bold'), fg='#DAD5D6', bg="#4580D8", cursor='hand2', activebackground='papaya whip')
        self.btnNuevo.grid(column=0, row=7, padx=10, pady= 5)

        self.btnGuardar = tk.Button(self, text= 'Guardar', command=self.guardarPaciente)
        self.btnGuardar.config(width=20, font=('APTOS DISPLAY',12,'bold'), fg='#DAD5D6', bg="#1DB92A", cursor='hand2', activebackground='papaya whip')
        self.btnGuardar.grid(column=1, row=7, padx=10, pady= 5)

        self.btnCancelar = tk.Button(self, text= 'Cancelar', command=self.deshabilitar)
        self.btnCancelar.config(width=20, font=('APTOS DISPLAY',12,'bold'), fg='#DAD5D6', bg="#D42727", cursor='hand2', activebackground='papaya whip')
        self.btnCancelar.grid(column=2, row=7, padx=10, pady= 5)

        self.btn_generar_pdf = tk.Button(self, text="Imprimir Historia", command=self.Imprimir_historia)
        self.btn_generar_pdf.config(width=20, font=('APTOS DISPLAY', 12, 'bold'), fg='#DAD5D6', bg="#6B37CC", cursor='hand2', activebackground='papaya whip')
        self.btn_generar_pdf.grid(column=4, row=7, padx=10, pady=5)

        # Deshabilitar o habilitar botones según el rol
        if self.rol == "Usuario":
            self.btnEditarPaciente.config(state="disabled")
            self.btnEliminarPaciente.config(state="disabled")
            
        elif self.rol == "Admin":
            self.btnNuevo.config(state="normal")
            self.btnGuardar.config(state="normal")
            self.btnCancelar.config(state="normal")
            self.btnEditarPaciente.config(state="normal")
            self.btnEliminarPaciente.config(state="normal")
            self.btnBuscarCondicion.config(state="normal")
            self.btnLimpiarBuscador.config(state="normal")
            self.btn_generar_pdf.config(state="normal")
            self.btnHistorialPaciente.config(state="normal")
            self.btnPlanTratamiento.config(state="normal")
            self.btnSalir.config(state="normal")

    def historiaClinica(self):
        try:
            sel = self.tabla.selection()
            if not sel:
                messagebox.showerror("Error", "Debe seleccionar un paciente.")
                return

            item = self.tabla.item(sel)
            valores = item['values']
            ci_str = str(valores[0])
            if not ci_str.isdigit():
                messagebox.showerror("Error", f"CI inválido: {ci_str}")
                return
            CI_original = int(ci_str)

            # Ventana ajustada para mejor visualización
            self.topHistoriaClinica = Toplevel()
            self.topHistoriaClinica.title('HISTORIA CLINICA')
            self.topHistoriaClinica.resizable(0, 0)
            self.topHistoriaClinica.config(bg='papaya whip')
            self.centrarVentana(self.topHistoriaClinica, 900, 450)  # Ventana más pequeña
            self.topHistoriaClinica.iconbitmap(r'C:\Users\Efrain\Desktop\ProyectoHistoria\Historias\img\Icono.ico')

            self.listahistoria = listarHistoria(CI_original) or []

            self.topHistoriaClinica.transient(self)
            self.topHistoriaClinica.grab_set()
            self.topHistoriaClinica.lift()
            self.topHistoriaClinica.focus_force()

            if self.listahistoria:
                grupo_id = self.listahistoria[0][0]
            else:
                grupo_id = None

            # Frame principal usando pack para mejor control del espacio
            main_frame = tk.Frame(self.topHistoriaClinica, bg='papaya whip')
            main_frame.pack(expand=True, fill='both', padx=10, pady=10)

            # Frame superior para tabla e imagen
            top_frame = tk.Frame(main_frame, bg='papaya whip')
            top_frame.pack(expand=True, fill='both', padx=5, pady=5)

            # Frame para la tabla (izquierda) con ancho fijo
            frame_tabla = tk.Frame(top_frame, bg='papaya whip', width=550)
            frame_tabla.pack(side='left', fill='both', expand=True, padx=5)
            frame_tabla.pack_propagate(False)

            # Frame para la imagen (derecha) con ancho fijo
            frame_imagen = tk.Frame(top_frame, bg='papaya whip', width=300)
            frame_imagen.pack(side='right', fill='both', padx=5)
            frame_imagen.pack_propagate(False)

            # Contenedor para tabla y scrollbar
            tabla_container = tk.Frame(frame_tabla)
            tabla_container.pack(fill='both', expand=True, padx=5, pady=5)

            # TABLA DE HISTORIAS
            self.tablaHistoria = ttk.Treeview(
                tabla_container,
                columns=('Nro Historia', 'Tratamiento', 'FechaHistoria', 'Odontologo'),
                show='headings',
                height=8  # Limitar número de filas visibles
            )
            
            # Encabezados y anchos de columna ajustados
            self.tablaHistoria.heading('Nro Historia', text='Nro Historia')
            self.tablaHistoria.heading('Tratamiento', text='Tratamiento')
            self.tablaHistoria.heading('FechaHistoria', text='Fecha')
            self.tablaHistoria.heading('Odontologo', text='Odontólogo')
            
            self.tablaHistoria.column('Nro Historia', width=80, anchor=W)
            self.tablaHistoria.column('Tratamiento', width=200, anchor=W)
            self.tablaHistoria.column('FechaHistoria', width=80, anchor=W)
            self.tablaHistoria.column('Odontologo', width=120, anchor=W)

            # Scrollbar integrado con la tabla
            scroll = ttk.Scrollbar(tabla_container, orient='vertical', command=self.tablaHistoria.yview)
            self.tablaHistoria.configure(yscrollcommand=scroll.set)
            
            # Empaquetar tabla y scrollbar juntos
            self.tablaHistoria.pack(side='left', fill='both', expand=True)
            scroll.pack(side='right', fill='y')

            # Llenar la tabla
            for p in self.listahistoria:
                self.tablaHistoria.insert('', 'end', values=(p[0], p[2], p[3], p[4]))

            # Bind para selección de historia
            self.tablaHistoria.bind('<<TreeviewSelect>>', lambda e: self.mostrar_imagen_historia(CI_original))

            # Frame para campos y botones (debajo de la tabla)
            bottom_frame = tk.Frame(main_frame, bg='papaya whip')
            bottom_frame.pack(fill='x', padx=5, pady=5)

            # CAMPOS DE ENTRADA
            vcmd = (self.topHistoriaClinica.register(lambda s: s == "" or s.isdigit()), '%P')

            # Frame para los campos
            frame_campos = tk.Frame(bottom_frame, bg='papaya whip')
            frame_campos.pack(fill='x', pady=5)

            # ID Historia
            tk.Label(frame_campos, text="Numero Historia:", font=('APTOS DISPLAY',11), bg='papaya whip').grid(row=0, column=0, sticky=W, padx=5, pady=2)
            self.svNumeroHistoria = tk.StringVar()
            self.entryNumeroHistoria = tk.Entry(frame_campos, textvariable=self.svNumeroHistoria, font=('APTOS DISPLAY',11), width=15, validate='key', validatecommand=vcmd)
            self.entryNumeroHistoria.grid(row=0, column=1, sticky=W, padx=5, pady=2)

            # Si el paciente ya tiene un número de historia, usarlo y deshabilitar el campo
            from Modelo.historiaClinicaDao import obtener_numero_historia_paciente
            numero_historia = obtener_numero_historia_paciente(CI_original)
            if numero_historia:
                self.svNumeroHistoria.set(str(numero_historia))
                self.entryNumeroHistoria.config(state='disabled')

            # Tratamiento
            tk.Label(frame_campos, text="Tratamiento:", font=('APTOS DISPLAY',11), bg='papaya whip').grid(row=0, column=2, sticky=W, padx=5, pady=2)
            self.svTratamiento = tk.StringVar()
            tk.Entry(frame_campos, textvariable=self.svTratamiento, font=('APTOS DISPLAY',11), width=25).grid(row=0, column=3, sticky=W, padx=5, pady=2)

            # Fecha Historia
            tk.Label(frame_campos, text="Fecha Historia:", font=('APTOS DISPLAY',11), bg='papaya whip').grid(row=1, column=0, sticky=W, padx=5, pady=2)
            self.svFechaHistoria = tk.StringVar()
            tk.Entry(frame_campos, textvariable=self.svFechaHistoria, font=('APTOS DISPLAY',11), width=15).grid(row=1, column=1, sticky=W, padx=5, pady=2)

            # Odontólogo
            tk.Label(frame_campos, text="Odontólogo:", font=('APTOS DISPLAY',11), bg='papaya whip').grid(row=1, column=2, sticky=W, padx=5, pady=2)
            self.svOdontologo = tk.StringVar()
            tk.Entry(frame_campos, textvariable=self.svOdontologo, font=('APTOS DISPLAY',11), width=25).grid(row=1, column=3, sticky=W, padx=5, pady=2)

            # BOTONES
            frame_botones = tk.Frame(bottom_frame, bg='papaya whip')
            frame_botones.pack(fill='x', pady=5)

            self.btnGuardarHistoria = tk.Button(frame_botones, text='Agregar Historia', width=15, font=('APTOS DISPLAY',12,'bold'),
                                              fg='#DAD5D6', bg='#1DB92A', cursor='hand2', activebackground='papaya whip',
                                              command=lambda: self._guardarHistoria(CI_original))
            self.btnGuardarHistoria.pack(side='left', padx=5, pady=5)

            self.btnEditarHistoria = tk.Button(frame_botones, text='Editar Historia', width=15, font=('APTOS DISPLAY',12,'bold'),
                                             fg='#DAD5D6', bg='#472FCF', cursor='hand2', activebackground='papaya whip',
                                             command=self.editarHistoria)
            self.btnEditarHistoria.pack(side='left', padx=5, pady=5)

            self.btnEliminarHistoria = tk.Button(frame_botones, text='Eliminar Historia', width=15, font=('APTOS DISPLAY',12,'bold'),
                                               fg='#DAD5D6', bg='#CE2929', cursor='hand2', activebackground='papaya whip',
                                               command=lambda: self._eliminarHistoria(CI_original))
            self.btnEliminarHistoria.pack(side='left', padx=5, pady=5)

            self.btnIngresarimagen = tk.Button(frame_botones, text='Cargar imagen', width=15, font=('APTOS DISPLAY',12,'bold'),
                                             fg='#DAD5D6', bg="#E94B0D", cursor='hand2', activebackground='papaya whip',
                                             command=self.cargar_imagen)
            self.btnIngresarimagen.pack(side='left', padx=5, pady=5)

            self.btnSalirHistoria = tk.Button(frame_botones, text='Salir', width=15, font=('APTOS DISPLAY',12,'bold'),
                                            fg='#DAD5D6', bg='#000000', cursor='hand2', activebackground='papaya whip',
                                            command=self.topHistoriaClinica.destroy)
            self.btnSalirHistoria.pack(side='left', padx=5, pady=5)

            # Deshabilitar botones si el rol es "Usuario"
            if self.rol == "Usuario":
                self.btnEditarHistoria.config(state="disabled")
                self.btnEliminarHistoria.config(state= "disabled")


            # Área de imagen con tamaño optimizado
            tk.Label(frame_imagen, text="Imagen Radiografia", font=('APTOS DISPLAY',12,'bold'), bg='papaya whip').pack(pady=5)
            
            # Frame contenedor de la imagen con tamaño más grande
            self.frame_imagen = tk.Frame(frame_imagen, bg='white', relief='sunken', bd=2, width=280, height=280)
            self.frame_imagen.pack(pady=5)
            self.frame_imagen.pack_propagate(False)  # Mantener tamaño fijo
            
            # Label para mostrar la imagen
            self.label_imagen = tk.Label(self.frame_imagen, bg='white', font=('APTOS DISPLAY',10), 
                                       text="Seleccione una historia\npara ver la imagen")
            self.label_imagen.pack(expand=True, fill='both')

        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def cargarDatosHistoria(self):
        seleccion = self.tablaHistoria.selection()
        if not seleccion:
            messagebox.showerror("Error", "Debe seleccionar una historia.")
            return

        item = self.tablaHistoria.item(seleccion)
        valores = item["values"]

        self.svTratamiento.set(valores[1])  
        self.svFechaHistoria.set(valores[2])  
        self.svOdontologo.set(valores[3])

    def mostrar_imagen_historia(self, ci_paciente):
        """Muestra la imagen asociada a la historia seleccionada"""
        try:
            seleccion = self.tablaHistoria.selection()
            if not seleccion:
                # Limpiar la imagen si no hay selección
                self.current_image = None
                self.label_imagen.config(image='', text="Seleccione una historia\npara ver la imagen")
                return

            item = self.tablaHistoria.item(seleccion)
            valores = item['values']
            fecha_historia = valores[2]  # La fecha está en la columna 2

            # Buscar imagen en la base de datos
            ruta_imagen = obtener_imagen_historia(ci_paciente, fecha_historia)
            
            if ruta_imagen and os.path.exists(ruta_imagen):
                # Cargar y redimensionar la imagen
                imagen_pil = Image.open(ruta_imagen)
                
                # Calcular el tamaño para mantener la proporción
                ancho_max, alto_max = 270, 270
                imagen_pil.thumbnail((ancho_max, alto_max), Image.Resampling.LANCZOS)
                
                # Convertir a PhotoImage y mantener referencia a nivel de clase
                self.current_image = ImageTk.PhotoImage(imagen_pil)
                
                # Mostrar la imagen
                self.label_imagen.config(image=self.current_image, text="")
            else:
                # No hay imagen o no existe el archivo
                self.current_image = None
                self.label_imagen.config(image='', text="No hay imagen\nasociada a esta historia")
                
        except Exception as e:
            print(f"Error al mostrar imagen: {e}")
            self.current_image = None
            self.label_imagen.config(image='', text="Error al cargar\nla imagen")

    def cargar_imagen(self):
        try:
            # Verificar selección de historia
            seleccion = self.tablaHistoria.selection()
            if not seleccion:
                messagebox.showerror("Error", "Debe seleccionar una historia primero.")
                return

            # Diálogo de archivo
            ruta = filedialog.askopenfilename(
                title="Seleccionar imagen periapical",
                filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.gif")]
            )
            if not ruta:
                return  # el usuario canceló

            # Obtener CI del paciente seleccionado en la tabla principal
            seleccion_paciente = self.tabla.selection()
            if not seleccion_paciente:
                messagebox.showerror("Error", "No se puede determinar el paciente.")
                return
            
            item_paciente = self.tabla.item(seleccion_paciente)
            ci_paciente = item_paciente['values'][0]  # CI del paciente

            # Obtener fecha de la historia seleccionada
            item = self.tablaHistoria.item(seleccion)
            valores = item['values']
            fecha = valores[2]  # Usar fecha de la historia seleccionada

            print(f"Guardando imagen para CI: {ci_paciente}, fecha: {fecha}")

            # Crear carpeta permanente si no existe
            carpeta_dest = os.path.join('imagenes', 'permanente')
            os.makedirs(carpeta_dest, exist_ok=True)

            # Generar nombre único para la imagen
            nombre = f"{ci_paciente}_{fecha.replace('-', '')}_{os.path.basename(ruta)}"
            destino = os.path.join(carpeta_dest, nombre)

            try:
                # Copiar imagen a carpeta permanente
                shutil.copy2(ruta, destino)

                # Guardar en base de datos
                guardar_imagen_historia(ci_paciente, fecha, destino)

                # Cargar y mostrar la imagen
                imagen_pil = Image.open(destino)
                imagen_pil.thumbnail((270, 270), Image.Resampling.LANCZOS)
                self.current_image = ImageTk.PhotoImage(imagen_pil)
                
                # Actualizar la imagen en el label
                self.label_imagen.config(image=self.current_image, text="")

                messagebox.showinfo("Éxito", "Imagen guardada correctamente.")

            except Exception as e:
                if os.path.exists(destino):
                    os.remove(destino)
                raise Exception(f"Error al procesar la imagen: {e}")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")
            return


  

    def es_fecha_valida(self, fecha):
        try:
            datetime.datetime.strptime(fecha, '%d-%m-%Y')
            return True
        except ValueError:
            return False


    def _guardarHistoria(self, CI):
        from Modelo.historiaClinicaDao import guardarHistoria, actualizarHistoria, listarHistoria, verificar_numero_historia_existe

        trat = self.svTratamiento.get().strip()
        fecha = self.svFechaHistoria.get().strip()
        odon = self.svOdontologo.get().strip()
        num_historia = self.svNumeroHistoria.get().strip()

        if not trat or not fecha or not odon or not num_historia:
            messagebox.showwarning("Validación", "Todos los campos son obligatorios.", parent=self.topHistoriaClinica)
            return
        
        if not self.es_fecha_valida(fecha):
            messagebox.showerror("Error", "La fecha ingresada no es válida. Use el formato DD-MM-YYYY.")
            return

        try:
            if self.historia_original is None:
                # Verificar si el número de historia ya existe para otro paciente
                if verificar_numero_historia_existe(num_historia, CI):
                    messagebox.showerror("Error", f"El número de historia {num_historia} ya está asignado a otro paciente.", parent=self.topHistoriaClinica)
                    return
                guardarHistoria(CI, num_historia, trat, fecha, odon)
                msg = "Historia clínica agregada correctamente."
                # Deshabilitar el campo después de guardar
                self.entryNumeroHistoria.config(state='disabled')
            else:
                actualizarHistoria(num_historia, CI, trat, fecha, odon)
                msg = "Historia clínica actualizada correctamente."

            self.listahistoria = listarHistoria(CI)
            self.tablaHistoria.delete(*self.tablaHistoria.get_children())
            for h in self.listahistoria:
                self.tablaHistoria.insert('', 'end', values=(h[0], h[2], h[3], h[4]))

            messagebox.showinfo("Éxito", msg, parent=self.topHistoriaClinica)
            
            self.svNumeroHistoria.set('')
            self.svTratamiento.set('')
            self.svFechaHistoria.set('')
            self.svOdontologo.set('')
            self.historia_original = None
            self.btnGuardarHistoria.config(text='Agregar Historia')
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar historia: {e}", parent=self.topHistoriaClinica)
            return

    
    def editarHistoria(self):
        sel = self.tablaHistoria.selection()
        if not sel:
            messagebox.showerror("Error", "Seleccione una historia para editar.", parent=self.topHistoriaClinica)
            return
        
        item = self.tablaHistoria.item(sel)
        valores = item['values']
       
        self.historia_original = valores[0]
        self.svTratamiento.set(valores[1])
        self.svFechaHistoria.set(valores[2])
        self.svOdontologo.set(valores[3])

        self.entryNumeroHistoria.config(state='disabled')
        self.btnGuardarHistoria.config(text="Guardar Cambios")

    def _eliminarHistoria(self, CI):
        from Modelo.historiaClinicaDao import eliminarHistoria, listarHistoria

        sel = self.tablaHistoria.selection()
        if not sel:
            messagebox.showerror("Error", "Seleccione una historia para eliminar.", parent=self.topHistoriaClinica)
            return

        item = self.tablaHistoria.item(sel)
        num_historia = item['values'][0]

        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar la historia #{num_historia}?", parent=self.topHistoriaClinica)
        if not confirm:
            return

        eliminarHistoria(num_historia, CI)

        self.listahistoria = listarHistoria(CI)
        self.tablaHistoria.delete(*self.tablaHistoria.get_children())
        for h in self.listahistoria:
            self.tablaHistoria.insert('', 'end', values=(h[0], h[2], h[3], h[4]))

        self.svNumeroHistoria.set('')
        self.svTratamiento.set('')
        self.svFechaHistoria.set('')
        self.svOdontologo.set('')
        messagebox.showinfo("Éxito", f"Historia #{num_historia} eliminada.", parent=self.topHistoriaClinica)


    def editarPaciente(self):
        try:
            seleccion = self.tabla.selection()
            if not seleccion:
                raise ValueError("No hay paciente seleccionado.")

            item = self.tabla.item(seleccion)
            valores = item['values']
        
            self.CI_original = valores[0]
            self.EdadPaciente = valores[1]
            self.TlfnPaciente = valores[2]
            self.NombrePaciente = item['text']
            self.AlergiaPaciente = valores[4]
            self.EnfermedadPaciente = valores[5]
            self.MedicamentoPaciente= valores[3]
        
            self.habilitar()

            self.entryCI.insert(0, self.CI_original)
            self.entryNombre.insert(0, self.NombrePaciente)
            self.entryEdad.insert(0, self.EdadPaciente)
            self.entryTlfn.insert(0, self.TlfnPaciente)
            self.entryEnfermedad.insert(0, self.EnfermedadPaciente)
            self.entryAlergia.insert(0, self.AlergiaPaciente)
            self.entryMedicamento.insert(0, self.MedicamentoPaciente) 

        except Exception as e:
            title = 'Editar Paciente'
            mensaje = f'Error al editar Paciente: {e}'
            messagebox.showerror(title, mensaje)

    def eliminarDatoPaciente(self):
        try:

            seleccion = self.tabla.selection()

            if not seleccion:
                messagebox.showwarning("Eliminar Paciente", "Por favor, selecciona un paciente de la lista.")
                return

            valores = self.tabla.item(seleccion)['values']
            CI = valores[0]  

            confirmacion = messagebox.askyesno(
                "Confirmar Eliminación", f"¿Estás seguro de que deseas eliminar al paciente con CI {CI}?"
        )
            if not confirmacion:
                return

            eliminarPaciente(CI)
        
            self.tablaPaciente()
            messagebox.showinfo("Éxito", f"El paciente con CI {CI} fue eliminado correctamente.")

        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error al eliminar el paciente: {e}")
    
    def abrirPlanTratamiento(self):
        try:
            if hasattr(self, 'topPlanTratamiento') \
            and self.topPlanTratamiento.winfo_exists():
                self.topPlanTratamiento.lift()
                self.topPlanTratamiento.focus_force()
            sel = self.tabla.selection()
        
            seleccion = self.tabla.selection()
            if not seleccion:
                messagebox.showerror("Error", "Debe seleccionar un paciente.")
                return

            item = self.tabla.item(seleccion)
            valores = item["values"]
            ci_str = str(valores[0])
            if not ci_str.isdigit():
                messagebox.showerror("Error", f"CI inválido: {ci_str}")
                return
            CI_original = int(ci_str)

            self.topPlanTratamiento = tk.Toplevel()
            self.topPlanTratamiento.title("PLAN DE TRATAMIENTO")
            self.topPlanTratamiento.geometry("730x350")
            self.centrarVentana(self.topPlanTratamiento, 720, 350)
            self.topPlanTratamiento.config(bg="papaya whip")
            self.topPlanTratamiento.transient(self)    
            self.topPlanTratamiento.grab_set()         
            self.topPlanTratamiento.lift()             
            self.topPlanTratamiento.focus_force()
            self.topPlanTratamiento.iconbitmap(r'C:\Users\Efrain\Desktop\ProyectoHistoria\Historias\img\Icono.ico')    
            self.topPlanTratamiento.resizable(False, False)  

            plan = obtenerPlanTratamiento(CI_original)

            frame_entrys = tk.Frame(self.topPlanTratamiento, bg="papaya whip")
            frame_entrys.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

            frame_botones = tk.Frame(self.topPlanTratamiento, bg="papaya whip")
            frame_botones.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

            frame_entrys.grid_columnconfigure(0, weight=1, minsize=100)  
            frame_entrys.grid_columnconfigure(1, weight=3, minsize=300)  
            self.plan_existe = bool(plan)

            self.entrys_plan = {}

            campos = [("R1:", "R1"), ("R2:", "R2"), ("R3:", "R3"), ("R4:", "R4"),
                    ("Limpieza:", "limpieza"), ("Extracción:", "extraccion"), ("Otros:", "otros"), ("Nota:", "Nota")]

            for idx, (label_text, campo) in enumerate(campos):
                tk.Label(
                    frame_entrys,
                    text=label_text,
                    font=("APTOS DISPLAY", 11),
                    bg="papaya whip"
                ).grid(row=idx, column=0, padx=10, pady=5, sticky="w")

                if plan:
                    valor_inicial = plan[idx] or ""
                else:
                    valor_inicial = ""

                entry = tk.Entry(
                    frame_entrys,
                    font=("APTOS", 12),
                    width=50
                )
                entry.insert(0, valor_inicial)

                if plan:
                    entry.config(state="disabled")

                entry.grid(row=idx, column=1, padx=(10, 20), pady=5, sticky="ew")
                self.entrys_plan[campo] = entry

            frame_btn = tk.Frame(self.topPlanTratamiento, bg="papaya whip")
            frame_btn.grid(row=1, column=0, columnspan=4, sticky="ew", padx=10, pady=10)
            for col in range(4):  
                frame_botones.grid_columnconfigure(col, weight=1, minsize=150)

            texto = "Guardar Cambios" if self.plan_existe else "Guardar Plan"
            self.btn_guardar = tk.Button(
                frame_btn, text=texto, font=("APTOS DISPLAY",12,"bold"),
                fg="#DAD5D6", bg="#1DB92A", width=15, cursor='hand2',
                command=lambda: self._guardarPlan(CI_original), activebackground='papaya whip'
            )
            self.btn_guardar.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

            btn_editar = tk.Button(
                frame_btn, text="Editar Plan", font=("APTOS DISPLAY",12,"bold"),
                fg="#DAD5D6", bg="#472FCF", width=15, cursor='hand2',
                command=self.editarPlanDeTratamiento, activebackground='papaya whip'
            )
            btn_editar.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

            btn_eliminar = tk.Button(
                frame_btn, text="Eliminar Plan", font=("APTOS DISPLAY",12,"bold"),
                fg="#DAD5D6", bg="#CE2929", width=15, cursor='hand2',
                command=lambda: self.eliminarPlanDeTratamiento(CI_original), activebackground='papaya whip'
            )
            btn_eliminar.grid(row=0, column=2, padx=5, pady=10, sticky="ew")

            btn_salir = tk.Button(
                frame_btn, text="Salir", font=("APTOS DISPLAY",12,"bold"),
                fg="#DAD5D6", bg="#000000", width=15, cursor='hand2',
                command=self.topPlanTratamiento.destroy, activebackground='papaya whip'
            )
            btn_salir.grid(row=0, column=3, padx=5, pady=10, sticky="ew")

            if self.rol == "Usuario":
                btn_eliminar.config(state="disabled")
                btn_editar.config(state= "disabled")

        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)


    def editarPlanDeTratamiento(self):
        for entry in self.entrys_plan.values():
            entry.config(state="normal")
        self.btn_guardar.config(text="Guardar Cambios")


    def _guardarPlan(self, ci):
        datos = {k: e.get() for k, e in self.entrys_plan.items()}
        try:
            guardarPlanTratamiento(ci, datos)
            messagebox.showinfo("Éxito", "Plan de tratamiento guardado.", parent=self.topPlanTratamiento)
            for entry in self.entrys_plan.values():
                entry.config(state="disabled")
            self.btn_guardar.config(text="Guardar Plan")
        except Exception as e:
            messagebox.showerror("Error", f"No se guardó: {e}", parent=self.topPlanTratamiento)
    
    def eliminarPlanDeTratamiento(self, ci):
        confirm = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar el plan de tratamiento del paciente con CI {ci}?",
            parent=self.topPlanTratamiento
        )
        if not confirm:
            return

        from Modelo.planTratamientoDao import eliminarPlanTratamiento
        eliminarPlanTratamiento(ci)

        messagebox.showinfo(
            "Plan eliminado",
            "El plan de tratamiento se eliminó correctamente.",
            parent=self.topPlanTratamiento
        )
        for entry in self.entrys_plan.values():
            entry.config(state="normal")
            entry.delete(0, tk.END) 

        self.plan_existe = False
        self.btn_guardar.config(text="Guardar Plan")


    def centrarVentana(self, ventana, ancho, alto):
            """
            Centra una ventana en la pantalla principal.
            
            Args:
                ventana (tk.Toplevel | tk.Tk): La ventana que quieres centrar.
                ancho (int): Ancho de la ventana.
                alto (int): Alto de la ventana.
            """
            ventana.update_idletasks()  
            ancho_pantalla = ventana.winfo_screenwidth()
            alto_pantalla = ventana.winfo_screenheight()
            x = (ancho_pantalla // 2) - (ancho // 2)
            y = (alto_pantalla // 2) - (alto // 2)
            ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def confirmar_cierre(self):
        import HistoriaClinica
        if messagebox.askyesno("Confirmar cierre", "¿Estás seguro de que deseas salir del sistema?"):
            if not HistoriaClinica.is_logging_in:
                self.root.destroy()
            else:
                self.root.destroy()

    def validar_campos(self, *campos):
            """Valida que los campos no estén vacíos.
            
            Args:
                *campos: Widgets Entry que se desean validar.
                
            Returns:
                bool: True si todos los campos tienen datos, False si alguno está vacío.
            """
            for campo in campos:
                if not campo.get().strip():  # Verifica si el texto está vacío o son solo espacios
                    return False
            return True
