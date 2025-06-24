import tkinter as tk
import ttkbootstrap as ttk
import menu

from tkinter import messagebox
from funciones import load_users, save_users

def open_register_window(parent):
    register_win = ttk.Toplevel(parent)
    register_win.title("Registrar Vendedor")
    register_win.geometry("700x500")

    menu.add_file_menu(register_win)

    tk.Label(register_win, text="Vendedor:").grid(row=0, column=0, padx=10, pady=10)
    entry_username = tk.Entry(register_win)
    entry_username.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(register_win, text="Contraseña:").grid(row=1, column=0, padx=10, pady=10)
    entry_password = tk.Entry(register_win, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(register_win, text="Nivel:").grid(row=2, column=0, padx=10, pady=10)
    nivel_var = tk.StringVar(value="Vendedor")
    tk.Radiobutton(register_win, text="Administrador", variable=nivel_var, value="admin").grid(row=2, column=1, sticky="w")
    tk.Radiobutton(register_win, text="Vendedor", variable=nivel_var, value="Vendedor").grid(row=3, column=1, sticky="w")

    def register_user():
        username = entry_username.get()
        password = entry_password.get()
        nivel = nivel_var.get()

        users = load_users()
        if username in users:
            messagebox.showerror("Error", "El usuario ya existe")
        else:
            users[username] = {"password": password, "nivel": nivel}
            save_users(users)
            messagebox.showinfo("Registro exitoso", f"Usuario {username} registrado como {nivel}")
            register_win.destroy()

    btn_register = ttk.Button(register_win, text="Registrar", command=register_user)
    btn_register.grid(row=4, column=0, columnspan=2, pady=10)

