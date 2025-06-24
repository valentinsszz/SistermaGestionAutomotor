import ttkbootstrap as ttk
import tkinter as tk
import menu
import json
import csv

from tkinter import messagebox, filedialog
import os
from funciones import load_users, save_users
from funciones import update_user

def open_manage_users_window(parent):
    manage_win = ttk.Toplevel(parent)
    manage_win.title("Gestionar Usuarios")
    manage_win.geometry("700x500")

    menu.add_file_menu(manage_win)

    users = load_users()

    lbl_info = tk.Label(manage_win, text="Usuarios registrados:")
    lbl_info.pack(pady=5)

    listbox = tk.Listbox(manage_win)
    listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def refresh_list():
        listbox.delete(0, tk.END)
        for user in users:
            nivel = users[user]["nivel"]
            listbox.insert(tk.END, f"{user} - {nivel}")

    def edit_user():
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona un usuario para editar")
            return
        index = selected[0]
        username = list(users.keys())[index]
        user_data = users[username]

        # Nueva ventana para editar usuario
        edit_win = ttk.Toplevel(manage_win)
        edit_win.title(f"Editar usuario: {username}")
        edit_win.geometry("300x200")
        edit_win.grab_set()

        tk.Label(edit_win, text="Nueva contraseña:").pack(pady=5)
        entry_password = tk.Entry(edit_win, show="*")
        entry_password.pack(pady=5)
        entry_password.insert(0, user_data["password"])

        tk.Label(edit_win, text="Nuevo nivel:").pack(pady=5)
        nivel_var = tk.StringVar(value=user_data["nivel"])
        tk.Radiobutton(edit_win, text="Administrador", variable=nivel_var, value="admin").pack()
        tk.Radiobutton(edit_win, text="Vendedor", variable=nivel_var, value="Vendedor").pack()

        def save_changes():
            new_password = entry_password.get()
            new_level = nivel_var.get()
            if not new_password:
                messagebox.showerror("Error", "La contraseña no puede estar vacia")
                return
            users[username]["password"] = new_password
            users[username]["nivel"] = new_level
            
            update_user(username, new_password, new_level)
            messagebox.showinfo("Éxito", f"Usuario {username} actualizado")
            refresh_list()
            edit_win.destroy()

        btn_save = ttk.Button(edit_win, text="Guardar cambios", command=save_changes)
        btn_save.pack(pady=10)

    def delete_user():
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona un usuario para eliminar")
            return
        index = selected[0]
        username = list(users.keys())[index]

        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar usuario {username}?")
        if confirm:
            del users[username]
            save_users(users)
            messagebox.showinfo("Éxito", f"Usuario {username} eliminado")
            refresh_list()

    def exportar_json_a_csv():
        try:
            ruta_csv = filedialog.asksaveasfilename(
            title="Guardar como",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")])
            if not ruta_csv:
                           return
            ruta_json = os.path.join("BaseDatos", "usuarios.json")
            with open(ruta_json, "r", encoding="utf-8") as archivo_json:
                   datos_json = json.load(archivo_json)
            datos_para_csv =[] 
            for username, datos in datos_json.items():
                       fila = {"usuario": username}
                       fila.update(datos)
                       datos_para_csv.append(fila)
                       with open(ruta_csv, "w", newline="", encoding="utf-8") as archivo_csv:
                               campos = datos_para_csv[0].keys()
                               writer = csv.DictWriter(archivo_json, fieldnames=campos)
                               writer.writeheader()
                               writer.writerows(datos_para_csv)
                               messagebox.showinfo("Éxito", f"Exportado correctamente a:\n{ruta_csv}")
        except Exception as e:
                               messagebox.showerror("Error", f"Ocurrió un error:\n{e}")


    btn_edit = ttk.Button(manage_win, text="Editar usuario", command=edit_user)
    btn_edit.pack(side=tk.LEFT, padx=10, pady=10)

    btn_delete = ttk.Button(manage_win, text="Eliminar usuario", command=delete_user)
    btn_delete.pack(side=tk.LEFT, padx=10, pady=10)
    
    btn_exportar = tk.Button(manage_win, text="Exportar usuarios.json a CSV", command=exportar_json_a_csv)
    btn_exportar.pack(side=tk.LEFT, padx=10, pady=10)
    refresh_list()
