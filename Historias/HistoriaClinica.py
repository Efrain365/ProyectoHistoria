import tkinter as tk
from paciente.gui import Frame
from Modelo.Login_GUI import LoginWindow  
from Modelo.LoginDAO import LoginDAO_

def main():
    # Crear ventana raíz
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal al inicio

    # Mostrar ventana de inicio de sesión
    login_window = LoginWindow(root)
    root.wait_window(login_window)  # Esperar hasta que se cierre la ventana de login

    # Si las credenciales son válidas, inicializar la ventana principal
    root.title('HISTORIA CLINICA')
    root.resizable(0, 0)
    frame = Frame(root)
    frame.mainloop()

if __name__ == '__main__':
    main()
