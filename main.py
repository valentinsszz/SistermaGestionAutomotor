#Todos mis imports
import ttkbootstrap as ttk
import tkinter as tk
import winsound
import menu
import os
#Y aca todas las funcioens que importo
from funciones import login
from main_window import open_main_window
from funciones import load_remembered_user
from funciones import save_remembered_user


# Crear ventana principal

root = ttk.Window(themename="superhero")
root.title("Login")
root.geometry("700x500")
root.minsize(700, 500)
winsound.PlaySound("./start.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

def on_close_session():
    root.deiconify()

menu.add_file_menu(root, on_close_session=on_close_session)

# Etiquetas y entradas
tk.Label(root, text="Usuario:").grid(row=0, column=0, padx=10, pady=10)
entry_username = tk.Entry(root)
entry_username.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Contraseña:").grid(row=1, column=0, padx=10, pady=10)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=10)

remember_var = tk.IntVar()
chk_remember = tk.Checkbutton(root, text="Recordar usuario y contraseña", variable=remember_var)
chk_remember.grid(row=2, column=1, padx=10, pady=10, sticky="w")

def on_login():
    username = entry_username.get()
    password = entry_password.get()
    nivel = login(username, password)
    if nivel:
        if remember_var.get() == 1:            
            save_remembered_user(username, password)
        else:
         
            if os.path.exists("remembered_user.json"):
                os.remove("remembered_user.json")
        root.withdraw()
        open_main_window(nivel)

# Botones
btn_login = tk.Button(root, text="Iniciar sesion", command=on_login)
btn_login.grid(row=3, column=0, padx=10, pady=10)

def load_remembered():    
    user, pwd = load_remembered_user()
    if user and pwd:
        entry_username.insert(0, user)
        entry_password.insert(0, pwd)
        remember_var.set(1)

load_remembered()

try:
    root.mainloop()
except KeyboardInterrupt:
    print("Ventana cerrada por el usuario (Ctrl + C)")
    root.destroy()  # Cierra la ventana correctamente

