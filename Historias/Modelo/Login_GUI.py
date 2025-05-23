import sys
import tkinter as tk
from tkinter import Image, messagebox
from Modelo.LoginDAO import LoginDAO_
from PIL import Image, ImageTk


class LoginWindow(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.dao = LoginDAO_()
        self.geometry("375x220")
        self.title("INICIAR SESIÓN")
        self.config(bg='papaya whip')
        self.resizable(0, 0)
        self.centrarVentana(self, 375, 220)

        self.protocol("WM_DELETE_WINDOW", self.close_window)

        # Imagen en la parte superior
        img = Image.open(r"C:\Users\Efrain\Desktop\CARPETA GLOWADENT\Horizontal-Transparente-1.png")
        img = img.resize((250, 50))  
        self.image = ImageTk.PhotoImage(img)

        self.lblImagen = tk.Label(self, image=self.image, bg='papaya whip')
        self.lblImagen.grid(row=0, column=0, columnspan=2, pady=(10, 20))  # Imagen con margen inferior

        # Etiqueta y entrada de Usuario
        self.lblUsuario = tk.Label(self, text="Usuario:", font=('APTOS', 11, 'bold'), bg='papaya whip')
        self.lblUsuario.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entryUsuario = tk.Entry(self, font=("APTOS", 12), width=20)
        self.entryUsuario.grid(row=1, column=1, padx=10, pady=5)

        # Etiqueta y entrada de Contraseña
        self.lblPassword = tk.Label(self, text="Contraseña:", font=('APTOS', 11, 'bold'), bg='papaya whip')
        self.lblPassword.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entryPassword = tk.Entry(self, show="*", font=("APTOS", 12), width=20)
        self.entryPassword.grid(row=2, column=1, padx=10, pady=5)

        # Botón de Iniciar Sesión
        self.btnLogin = tk.Button(self, text="Iniciar Sesión",
                                  width=13, font=('ARIAL', 12, 'bold'),
                                  fg='#DAD5D6', bg="#08A52A",
                                  cursor='hand2', activebackground='papaya whip', command=self.validar_credenciales)
        self.btnLogin.grid(row=3, column=0, padx=10, pady=15, sticky="w")

        # Botón de Salir
        self.btnSalir = tk.Button(self, text="Salir", width=13, font=('ARIAL', 12, 'bold'),
                                  fg='#DAD5D6', bg="#000000",
                                  cursor='hand2', activebackground='papaya whip', command=self.close_window)
        self.btnSalir.grid(row=3, column=1, padx=10, pady=15, sticky="e")


    

    def close_window(self):
        if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?"):
            self.destroy()  
            sys.exit()

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

    def validar_credenciales(self):
        usuario = self.entryUsuario.get()
        password = self.entryPassword.get()
        if self.dao.validar_credenciales(usuario, password):
            self.destroy()  # Cerrar la ventana de inicio de sesión
            self.root.deiconify()  # Mostrar la ventana principal
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")