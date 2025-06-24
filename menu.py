import tkinter as tk

def add_file_menu(window, on_close_session=None):
    menubar = tk.Menu(window)
    file_menu = tk.Menu(menubar, tearoff=0)
    if on_close_session:
        file_menu.add_command(label="Cerrar sesión", command=on_close_session)
    file_menu.add_command(label="Salir", command=window.destroy)
    menubar.add_cascade(label="Archivo", menu=file_menu)
    window.config(menu=menubar)
