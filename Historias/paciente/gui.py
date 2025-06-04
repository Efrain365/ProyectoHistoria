import tkinter as tk
from tkinter import *
from tkinter import ttk, Toplevel
from tkinter import messagebox
from Modelo.planTratamientoDao import guardarPlanTratamiento, obtenerPlanTratamiento
from Modelo.PacienteDao import Persona, listarCondicion, listar, eliminarPaciente
from Modelo.historiaClinicaDao import listarHistoria
from paciente.gui import Frame
import sys

class Frame(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=1280, height=720)
        self.CI_original = None
        self.historia_original = None       
        self.root = root
        self.pack()
        self.config(bg='papaya whip')
        self.campospaciente()
        self.deshabilitar()
        self.tablaPaciente()
        self.root.protocol("WM_DELETE_WINDOW", self.confirmar_cierre)
        self.centrarVentana(root, 1280, 585)

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
        if not self.validar_campos(self.entryBuscarNombre, self.entryBuscarCI):
            messagebox.showerror("Error", "Debe ingresar alguna cedula o nombre para buscar pacientes")
            return
        
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
        if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?"):
            self.destroy()  
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

        self.btnEditarPaciente = tk.Button(self, text='Editar Paciente', command=self.editarPaciente)
        self.btnEditarPaciente.config(width= 20, font=('APTOS',12,'bold'), fg='#DAD5D6', bg='#1E0075', activebackground='#9379E0', cursor='hand2')
        self.btnEditarPaciente.grid(row=9, column=0, padx=10, pady=5)

        self.btnEliminarPaciente = tk.Button(self, text='Eliminar Paciente', command= self.eliminarDatoPaciente)
        self.btnEliminarPaciente.config(width= 20, font=('APTOS',12,'bold'), fg='#DAD5D6', bg='#8A0000', activebackground='#D58A8A', cursor='hand2')
        self.btnEliminarPaciente.grid(row=9, column=1, padx=10, pady=5)

        self.btnHistorialPaciente = tk.Button(self, text='Historial Paciente', command= self.historiaClinica)
        self.btnHistorialPaciente.config(width= 20, font=('APTOS',12,'bold'), fg='#DAD5D6', bg='#007C79', activebackground='#99F2F0', cursor='hand2')
        self.btnHistorialPaciente.grid(row=9, column=2, padx=10, pady=5) 

        self.btnPlanTratamiento = tk.Button( self, text='Plan de Tratamiento', command= self.abrirPlanTratamiento)
        self.btnPlanTratamiento.config(width=20, font=('ARIAL',12,'bold'),fg='#DAD5D6', bg='#AA4A44',activebackground='papaya whip',cursor='hand2')
        self.btnPlanTratamiento.grid(row=9, column=3, padx=10, pady=5)

        self.btnSalir = tk.Button(self, text='Salir', command= self.cerrarventana)
        self.btnSalir.config(width= 20, font=('APTOS',12,'bold'), fg='#DAD5D6', bg='#000000', activebackground='#99F2F0', cursor='hand2')
        self.btnSalir.grid(row=9, column=4, padx=10, pady=5)

    def historiaClinica(self):
        try:
            sel = self.tabla.selection()
            if not sel:
                messagebox.showerror("Error", "Debe seleccionar un paciente.")
                return

            item    = self.tabla.item(sel)
            valores = item['values']
            ci_str  = str(valores[0])
            if not ci_str.isdigit():
                messagebox.showerror("Error", f"CI inválido: {ci_str}")
                return
            CI_original = int(ci_str)
 
            # Ventana
            self.topHistoriaClinica = Toplevel()
            self.topHistoriaClinica.title('HISTORIA CLINICA')
            self.topHistoriaClinica.resizable(0, 0)
            self.topHistoriaClinica.config(bg='papaya whip')
            self.centrarVentana(self.topHistoriaClinica, 760, 360)

            self.listahistoria = listarHistoria(CI_original) or []

            self.topHistoriaClinica.transient(self)  
            self.topHistoriaClinica.grab_set()     
            self.topHistoriaClinica.lift()          
            self.topHistoriaClinica.focus_force()

            if self.listahistoria:
                grupo_id = self.listahistoria[0][0]  
            else:
                grupo_id = None

            for col in range(4):
                self.topHistoriaClinica.grid_columnconfigure(col, weight=1)

            self.tablaHistoria = ttk.Treeview(
                self.topHistoriaClinica,
                columns=('ID', 'Tratamiento', 'FechaHistoria', 'Odontologo'),
                show='headings'
            )
            
            # Encabezados
            self.tablaHistoria.heading('ID',            text='ID')
            self.tablaHistoria.heading('Tratamiento',   text='Tratamiento')
            self.tablaHistoria.heading('FechaHistoria', text='Fecha')
            self.tablaHistoria.heading('Odontologo',    text='Odontólogo')
            # Anchos
            self.tablaHistoria.column('ID',            width=50,  anchor=W)
            self.tablaHistoria.column('Tratamiento',   width=400, anchor=W)
            self.tablaHistoria.column('FechaHistoria', width=100, anchor=W)
            self.tablaHistoria.column('Odontologo',    width=150, anchor=W)

            self.tablaHistoria.grid(row=0, column=0, columnspan=4, sticky='nse', padx=10, pady=10)

            # Scrollbar
            scroll = ttk.Scrollbar(
                self.topHistoriaClinica,
                orient='vertical',
                command=self.tablaHistoria.yview
            )
            scroll.grid(row=0, column=4, sticky='ns', pady=10, padx=0)
            self.tablaHistoria.configure(yscrollcommand=scroll.set)

            self.listahistoria = listarHistoria(CI_original) or []
            for p in self.listahistoria:
                # p = (idHistoriaClinica, Nombre, Tratamiento, Fecha, Odontologo)
                self.tablaHistoria.insert(
                    '', 'end',
                    values=(p[0], p[2], p[3], p[4])
                )

            vcmd = (self.topHistoriaClinica.register(lambda s: s == "" or s.isdigit()), '%P')

            tk.Label(self.topHistoriaClinica,
                    text="ID Historia:",
                    font=('APTOS',11,'bold'),
                    bg='papaya whip').grid(row=1, column=0, sticky=W, padx=10, pady=(5,0))

            self.svIDHistoria = tk.StringVar(value=str(grupo_id) if grupo_id else "")
            self.entryIDHistoria = tk.Entry(
                self.topHistoriaClinica,
                textvariable=self.svIDHistoria,
                font=('APTOS',12),
                width=15,
                validate='key', validatecommand=vcmd
            )
            self.entryIDHistoria.grid(row=1, column=1, sticky=W, padx=10)

            #Labels y entrys

            tk.Label(self.topHistoriaClinica,
                    text="ID Historia:",
                    font=('APTOS',11,'bold'),
                    bg='papaya whip').grid(row=1, column=0, sticky=W, padx=10, pady=(5,0))
            self.svIDHistoria = tk.StringVar()

            tk.Entry(self.topHistoriaClinica,
                    textvariable=self.svIDHistoria,
                    font=('APTOS',12),
                    width=15,
                    validate='key', validatecommand=vcmd
            ).grid(row=1, column=1, sticky=W, padx=10)

            tk.Label(self.topHistoriaClinica,
                    text="Tratamiento:",
                    font=('APTOS',11,'bold'),
                    bg='papaya whip').grid(row=1, column=2, sticky=W, padx=10, pady=(5,0))
            self.svTratamiento = tk.StringVar()
            tk.Entry(self.topHistoriaClinica,
                    textvariable=self.svTratamiento,
                    font=('APTOS',12),
                    width=25).grid(row=1, column=3, sticky= W, padx=10)

            tk.Label(self.topHistoriaClinica,
                    text="Fecha Historia:",
                    font=('APTOS',11,'bold'),
                    bg='papaya whip').grid(row=2, column=0, sticky=W, padx=10, pady=(5,0))
            self.svFechaHistoria = tk.StringVar()
            tk.Entry(self.topHistoriaClinica,
                    textvariable=self.svFechaHistoria,
                    font=('APTOS',12),
                    width=15).grid(row=2, column=1, padx=10, sticky=W, pady=(5,0))

            tk.Label(self.topHistoriaClinica,
                    text="Odontólogo:",
                    font=('APTOS',11,'bold'),
                    bg='papaya whip').grid(row=2, column=2, sticky=W, padx=10, pady=(5,0))
            self.svOdontologo = tk.StringVar()
            tk.Entry(self.topHistoriaClinica,
                    textvariable=self.svOdontologo,
                    font=('APTOS',12),
                    width=25).grid(row=2, column=3, padx=10, pady=(5,0))

            # Botones de las historias
            self.btnGuardarHistoria = tk.Button(
                self.topHistoriaClinica,
                text='Agregar Historia',
                width=15, font=('ARIAL',12,'bold'),
                fg='#DAD5D6', bg='#158645',
                cursor='hand2', activebackground='papaya whip',
                command=lambda: self._guardarHistoria(CI_original)
            )
            self.btnGuardarHistoria.grid(row=3, column=0, padx=10, pady=15)

            self.btnEditarHistoria = tk.Button(
                self.topHistoriaClinica,
                text='Editar Historia',
                width=15, font=('ARIAL',12,'bold'),
                fg='#DAD5D6', bg='#1E0075',
                cursor='hand2', activebackground='#9379E0',
                command= self.editarHistoria
            )
            self.btnEditarHistoria.grid(row=3, column=1, padx=10, pady=15)

            self.btnEliminarHistoria = tk.Button(
                self.topHistoriaClinica,
                text='Eliminar Historia',
                width=15, font=('ARIAL',12,'bold'),
                fg='#DAD5D6', bg='#8A0000',
                cursor='hand2', activebackground='#D58A8A',
                command=lambda: self._eliminarHistoria(CI_original)
            )
            self.btnEliminarHistoria.grid(row=3, column=2, padx=10, pady=15)

            self.btnSalirHistoria = tk.Button(
                self.topHistoriaClinica,
                text='Salir',
                width=15, font=('ARIAL',12,'bold'),
                fg='#DAD5D6', bg='#000000',
                cursor='hand2', activebackground='#99F2F0',
                command=self.topHistoriaClinica.destroy
            )
            self.btnSalirHistoria.grid(row=3, column=3, padx=10, pady=15)

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

    def _guardarHistoria(self, CI):
        from Modelo.historiaClinicaDao import guardarHistoria, actualizarHistoria, listarHistoria

        trat  = self.svTratamiento.get().strip()
        fecha = self.svFechaHistoria.get().strip()
        odon  = self.svOdontologo.get().strip()
        if not trat or not fecha or not odon:
            messagebox.showwarning("Validación", "Todos los campos son obligatorios.", parent=self.topHistoriaClinica)
            return

        if self.historia_original is None:
            guardarHistoria(CI, trat, fecha, odon)
            msg = "Historia clínica agregada correctamente."
        else:
            actualizarHistoria(self.historia_original, trat, fecha, odon)
            msg = "Historia clínica actualizada correctamente."

        self.listahistoria = listarHistoria(CI)
        self.tablaHistoria.delete(*self.tablaHistoria.get_children())
        for h in self.listahistoria:
            self.tablaHistoria.insert('', 'end', values=(h[0], h[2], h[3], h[4]))

        messagebox.showinfo("Éxito", msg, parent=self.topHistoriaClinica)

        self.entryIDHistoria.config(state='normal')

        
        self.svIDHistoria.set('')
        self.svTratamiento.set('')
        self.svFechaHistoria.set('')
        self.svOdontologo.set('')
        self.historia_original = None
        self.btnGuardarHistoria.config(text='Agregar Historia')

    
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

        self.entryIDHistoria.config(state='disabled')
        self.btnGuardarHistoria.config(text="Guardar Cambios")

    def _eliminarHistoria(self, CI):
        from Modelo.historiaClinicaDao import eliminarHistoria, listarHistoria

        sel = self.tablaHistoria.selection()
        if not sel:
            messagebox.showerror("Error", "Seleccione una historia para eliminar.", parent=self.topHistoriaClinica)
            return

        item = self.tablaHistoria.item(sel)
        idHistoria = item['values'][0]

        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar la historia #{idHistoria}?", parent=self.topHistoriaClinica)
        if not confirm:
            return

        eliminarHistoria(idHistoria)

        self.listahistoria = listarHistoria(CI)
        self.tablaHistoria.delete(*self.tablaHistoria.get_children())
        for h in self.listahistoria:
            self.tablaHistoria.insert('', 'end', values=(h[0], h[2], h[3], h[4]))

        self.svIDHistoria.set('')
        self.svTratamiento.set('')
        self.svFechaHistoria.set('')
        self.svOdontologo.set('')
        messagebox.showinfo("Éxito", f"Historia #{idHistoria} eliminada.", parent=self.topHistoriaClinica)


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
            self.centrarVentana(self.topPlanTratamiento, 720, 330)
            self.topPlanTratamiento.config(bg="papaya whip")
            self.topPlanTratamiento.transient(self)    
            self.topPlanTratamiento.grab_set()         
            self.topPlanTratamiento.lift()             
            self.topPlanTratamiento.focus_force()      
            self.topPlanTratamiento.resizable(False, False)  

            from Modelo.planTratamientoDao import obtenerPlanTratamiento
            plan = obtenerPlanTratamiento(CI_original)

            frame_entrys = tk.Frame(self.topPlanTratamiento, bg="papaya whip")
            frame_entrys.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

            frame_botones = tk.Frame(self.topPlanTratamiento, bg="papaya whip")
            frame_botones.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

            frame_entrys.grid_columnconfigure(0, weight=1, minsize=100)  
            frame_entrys.grid_columnconfigure(1, weight=3, minsize=300)  

            from Modelo.planTratamientoDao import obtenerPlanTratamiento
            plan = obtenerPlanTratamiento(CI_original)  
            self.plan_existe = bool(plan)

            self.entrys_plan = {}

            campos = [("R1:", "R1"), ("R2:", "R2"), ("R3:", "R3"), ("R4:", "R4"),
                    ("Limpieza:", "limpieza"), ("Extracción:", "extraccion"), ("Otros:", "otros")]

            for idx, (label_text, campo) in enumerate(campos):
                tk.Label(
                    frame_entrys,
                    text=label_text,
                    font=("APTOS", 11, "bold"),
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

                entry.grid(row=idx, column=1, padx=(10, 20), pady=5, sticky="ew")
                self.entrys_plan[campo] = entry

            frame_btn = tk.Frame(self.topPlanTratamiento, bg="papaya whip")
            frame_btn.grid(row=1, column=0, columnspan=4, sticky="ew", padx=10, pady=10)
            for col in range(4):  
                frame_botones.grid_columnconfigure(col, weight=1, minsize=150)

            texto = "Guardar Cambios" if self.plan_existe else "Guardar Plan"
            self.btn_guardar = tk.Button(
                frame_btn, text=texto, font=("ARIAL",12,"bold"),
                fg="#DAD5D6", bg="#158645", width=15, cursor='hand2',
                command=lambda: self._guardarPlan(CI_original)
            )
            self.btn_guardar.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

            btn_editar = tk.Button(
                frame_btn, text="Editar Plan", font=("ARIAL",12,"bold"),
                fg="#DAD5D6", bg="#1658a2", width=15, cursor='hand2',
                command=self.editarPlanDeTratamiento
            )
            btn_editar.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

            btn_eliminar = tk.Button(
                frame_btn, text="Eliminar Plan", font=("ARIAL",12,"bold"),
                fg="#DAD5D6", bg="#B00000", width=15, cursor='hand2',
                command=lambda: self.eliminarPlanDeTratamiento(CI_original)
            )
            btn_eliminar.grid(row=0, column=2, padx=5, pady=10, sticky="ew")

            btn_salir = tk.Button(
                frame_btn, text="Salir", font=("ARIAL",12,"bold"),
                fg="#DAD5D6", bg="#000000", width=15, cursor='hand2',
                command=self.topPlanTratamiento.destroy
            )
            btn_salir.grid(row=0, column=3, padx=5, pady=10, sticky="ew")

        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)

    def abrirPlanDeTratamiento(self):
        ventana_plan = tk.Toplevel()
        ventana_plan.title("PLAN DE TRATAMIENTO")
        ventana_plan.geometry("400x500")

        campos = ["R1", "R2", "R3", "R4", "Limpieza", "Extracción", "Otros"]
        self.entrys_plan = {}

        plan = obtenerPlanTratamiento(self.CI_original)

        for i, campo in enumerate(campos):
            label = tk.Label(ventana_plan, text=campo)
            label.grid(row=i, column=0, padx=10, pady=10)
            
            entry = tk.Entry(ventana_plan)
            entry.grid(row=i, column=1, padx=10, pady=10)

        btn_guardar = tk.Button(ventana_plan, text="Guardar", command=lambda: self.guardarPlanDeTratamiento())
        btn_guardar.grid(row=len(campos), column=0, columnspan=2, pady=20)

        self.btn_guardar = btn_guardar
        ventana_plan.mainloop()

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
        if messagebox.askyesno("Confirmar cierre", "¿Estás seguro de que deseas salir del sistema?"):
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