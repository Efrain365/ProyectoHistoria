from sqlite3 import Cursor
import tkinter as tk
from tkinter import *
from tkinter import Button, ttk, scrolledtext, Toplevel
from tkinter import messagebox
from Modelo.Conexion import ConexionDB
from Modelo.PacienteDao import Persona, actualizarPaciente, guardarDatoPaciente, listarCondicion, listar, eliminarPaciente


class Frame(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=1280, height=720)
        self.CI_original = None         # ← Aquí
        self.root = root
        self.pack()
        self.config(bg='papaya whip')
        self.campospaciente()
        self.deshabilitar()
        self.tablaPaciente()

 #LABELS

    def campospaciente(self):
        self.lblNombre = tk.Label(self, text= 'Nombre: ')
        self.lblNombre.config(font=('APTOS',14,'bold'), bg='papaya whip')
        self.lblNombre.grid(column=0, row=0, padx=10, pady= 5)

        self.lblCI = tk.Label(self, text= 'Cedula: ')
        self.lblCI.config(font=('APTOS',14,'bold'), bg='papaya whip')
        self.lblCI.grid(column=0, row=1, padx=10, pady= 5)

        self.lblEdad = tk.Label(self, text= 'Edad: ')
        self.lblEdad.config(font=('APTOS',14,'bold'), bg='papaya whip')
        self.lblEdad.grid(column=0, row=2, padx=10, pady= 5)

        self.lblTlfn = tk.Label(self, text= 'Telefono: ')
        self.lblTlfn.config(font=('APTOS',14,'bold'), bg='papaya whip')
        self.lblTlfn.grid(column=0, row=3, padx=10, pady= 5)

        self.lblAlergia = tk.Label(self, text= 'Alergia: ')
        self.lblAlergia.config(font=('APTOS',15,'bold'), bg='papaya whip')
        self.lblAlergia.grid(column=0, row=4, padx=10, pady= 5)

        self.lblEnfermedad = tk.Label(self, text= 'Enfermedad: ')
        self.lblEnfermedad.config(font=('APTOS',14,'bold'), bg='papaya whip')
        self.lblEnfermedad.grid(column=0, row=5, padx=10, pady= 5)

        self.lblMedicamento = tk.Label(self, text= 'Medicamento: ')
        self.lblMedicamento.config(font=('APTOS',14,'bold'), bg='papaya whip')
        self.lblMedicamento.grid(column=0, row=6, padx=10, pady= 5)

        #ENTRYS

        self.svNombre = tk.StringVar()
        self.entryNombre = tk.Entry(self, textvariable=self.svNombre)
        self.entryNombre.config(width=50, font=('APTOS',14))
        self.entryNombre.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

        self.svCI = tk.StringVar()
        self.entryCI = tk.Entry(self, textvariable=self.svCI)
        self.entryCI.config(width=50, font=('APTOS',14))
        self.entryCI.grid(column=1, row=1, padx=10, pady=5, columnspan=2)

        self.svEdad = tk.StringVar()
        self.entryEdad = tk.Entry(self, textvariable=self.svEdad)
        self.entryEdad.config(width=50, font=('APTOS',14))
        self.entryEdad.grid(column=1, row=2, padx=10, pady=5, columnspan=2)

        self.svTlfn = tk.StringVar()
        self.entryTlfn = tk.Entry(self, textvariable=self.svTlfn)
        self.entryTlfn.config(width=50, font=('APTOS',14))
        self.entryTlfn.grid(column=1, row=3, padx=10, pady=5, columnspan=2)

        self.svAlergia = tk.StringVar()
        self.entryAlergia = tk.Entry(self, textvariable=self.svAlergia)
        self.entryAlergia.config(width=50, font=('APTOS',14))
        self.entryAlergia.grid(column=1, row=4, padx=10, pady=5, columnspan=2)

        self.svEnfermedad = tk.StringVar()
        self.entryEnfermedad = tk.Entry(self, textvariable=self.svEnfermedad)
        self.entryEnfermedad.config(width=50, font=('APTOS',14))
        self.entryEnfermedad.grid(column=1, row=5, padx=10, pady=5, columnspan=2)

        self.svMedicamento = tk.StringVar()
        self.entryMedicamento = tk.Entry(self, textvariable=self.svMedicamento)
        self.entryMedicamento.config(width=50, font=('APTOS',14))
        self.entryMedicamento.grid(column=1, row=6, padx=10, pady=5, columnspan=2)

        #BUSCADOR

        #LABEL BUSCARDOR
        self.lblBuscarCI = tk.Label(self, text='Buscar CI: ')
        self.lblBuscarCI.config(font=('APTOS',14,'bold'), bg='papaya whip')
        self.lblBuscarCI.grid(column=3, row=0, padx=10, pady=5)

        self.lblBuscarNombre = tk.Label(self, text='Buscar Nombre: ')
        self.lblBuscarNombre.config(font=('APTOS',14,'bold'), bg='papaya whip')
        self.lblBuscarNombre.grid(column=3, row=1, padx=10, pady=5)

        #ENTRY BUSCADOR
        self.svBuscarCI = tk.StringVar()
        self.entryBuscarCI = tk.Entry(self, textvariable=self.svBuscarCI)
        self.entryBuscarCI.config(width=20, font=('APTOS',14))
        self.entryBuscarCI.grid(column=4, row=0, padx=10, pady=5, columnspan=2)

        self.svBuscarNombre = tk.StringVar()
        self.entryBuscarNombre = tk.Entry(self, textvariable=self.svBuscarNombre)
        self.entryBuscarNombre.config(width=20, font=('APTOS',14))
        self.entryBuscarNombre.grid(column=4, row=1, padx=10, pady=5, columnspan=2)

        #BUTTON BUSCADOR
        self.btnBuscarCondicion = tk.Button(self, text= 'Buscar', command= self.buscarCondicion)
        self.btnBuscarCondicion.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#00396F', cursor='hand2', activebackground='papaya whip')
        self.btnBuscarCondicion.grid(column=3, row=2, padx=10, pady= 5, columnspan= 1)

        self.btnLimpiarBuscador = tk.Button(self, text= 'Limpiar', command= self.LimpiarBuscador)
        self.btnLimpiarBuscador.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#120061', cursor='hand2', activebackground='papaya whip')
        self.btnLimpiarBuscador.grid(column=4, row=2, padx=10, pady= 5, columnspan= 1)

        #BUTTONS

        self.btnNuevo = tk.Button(self, text= 'Nuevo', command=self.habilitar)
        self.btnNuevo.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#1658a2', cursor='hand2', activebackground='papaya whip')
        self.btnNuevo.grid(column=0, row=7, padx=10, pady= 5)

        self.btnGuardar = tk.Button(self, text= 'Guardar', command=self.guardarPaciente)
        self.btnGuardar.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#158645', cursor='hand2', activebackground='papaya whip')
        self.btnGuardar.grid(column=1, row=7, padx=10, pady= 5)

        self.btnCancelar = tk.Button(self, text= 'Cancelar', command=self.deshabilitar)
        self.btnCancelar.config(width=20, font=('ARIAL',12,'bold'), fg='#DAD5D6', bg='#B00000', cursor='hand2', activebackground='papaya whip')
        self.btnCancelar.grid(column=2, row=7, padx=10, pady= 5)
    
        from Modelo.PacienteDao import guardarDatoPaciente, actualizarPaciente
    
    def LimpiarBuscador(self):
        self.svBuscarNombre.set('')
        self.svBuscarCI.set('')
        self.tablaPaciente()

    def buscarCondicion(self):
        if len(self.svBuscarCI.get()) > 0 or len(self.svBuscarNombre.get()) > 0:
            where = "WHERE 1=1" 
            if(len(self.svBuscarCI.get())) > 0:
                where = "WHERE CI = " + self.svBuscarCI.get() +""
            if (len(self.svBuscarNombre.get())) > 0:
                where = "WHERE Nombre LIKE '" + self.svBuscarNombre.get() + "%'"
            
            self.tablaPaciente(where)
        else:
            self.tablaPaciente()

    def guardarPaciente(self):
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

        self.btnEditarPaciente = tk.Button(self, text='Editar Paciente', command=self.editarPaciente)
        self.btnEditarPaciente.config(width= 20, font=('APTOS',12,'bold'), fg='#DAD5D6', bg='#1E0075', activebackground='#9379E0', cursor='hand2')
        self.btnEditarPaciente.grid(row=9, column=0, padx=10, pady=5)

        self.btnEliminarPaciente = tk.Button(self, text='Eliminar Paciente', command= self.eliminarDatoPaciente)
        self.btnEliminarPaciente.config(width= 20, font=('APTOS',12,'bold'), fg='#DAD5D6', bg='#8A0000', activebackground='#D58A8A', cursor='hand2')
        self.btnEliminarPaciente.grid(row=9, column=1, padx=10, pady=5)

        self.btnHistorialPaciente = tk.Button(self, text='Historia Paciente')
        self.btnHistorialPaciente.config(width= 20, font=('APTOS',12,'bold'), fg='#DAD5D6', bg='#007C79', activebackground='#99F2F0', cursor='hand2')
        self.btnHistorialPaciente.grid(row=9, column=2, padx=10, pady=5) 

        self.btnSalir = tk.Button(self, text='Salir', command=self.root.destroy)
        self.btnSalir.config(width= 20, font=('APTOS',12,'bold'), fg='#DAD5D6', bg='#000000', activebackground='#99F2F0', cursor='hand2')
        self.btnSalir.grid(row=9, column=4, padx=10, pady=5)

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
            self.EnfermedadPaciente = valores[4]
            self.AlergiaPaciente = valores[3]
            self.MedicamentoPaciente= valores[5]
        
            self.habilitar()

            self.entryCI.insert(0, self.CI_original)
            self.entryNombre.insert(0, self.NombrePaciente)
            self.entryEdad.insert(0, self.EdadPaciente)
            self.entryTlfn.insert(0, self.TlfnPaciente)
            self.entryEnfermedad.insert(0, self.EnfermedadPaciente)
            self.entryAlergia.insert(0, self.AlergiaPaciente)
            self.entryMedicamento.insert(0, self.MedicamentoPaciente) 

        except: 
            title = 'Editar Paciente'
            mensaje = 'Error al editar Paciente'
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

