import tkinter as tk
from paciente.gui import Frame
from Modelo.Login_GUI import LoginWindow  
from Modelo.LoginDAO import LoginDAO_

is_logging_in = True

def main():
    root = tk.Tk()
    root.withdraw()  
    root.iconbitmap(r'C:\Users\Efrain\Desktop\ProyectoHistoria\Historias\img\Icono.ico')
    login_window = LoginWindow(root)
    root.wait_window(login_window)

    # The Frame is created in Login_GUI.py after successful login
    # root.title('REGISTRAR PACIENTE')
    # root.resizable(0, 0)
    # frame = Frame(root)
    # frame.mainloop()

if __name__ == '__main__':
    main()
