import tkinter as tk
import ttkbootstrap as ttk
import menu
import os
import shutil
import json
import csv

from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from funciones import load_clients, add_client, update_client, delete_client

def open_clients_window(parent):
    clients_win = ttk.Toplevel(parent)
    clients_win.title("Gestionar Clientes")
    clients_win.geometry("700x600")

    menu.add_file_menu(clients_win)

    clients = load_clients()
    filtered_clients = clients.copy()

    lbl_search = tk.Label(clients_win, text="Buscar:")
    lbl_search.pack(pady=5)

    search_var = tk.StringVar()

    entry_search = tk.Entry(clients_win, textvariable=search_var)
    entry_search.pack(fill=tk.X, padx=10)

    listbox = tk.Listbox(clients_win)
    listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def refresh_list():
        listbox.delete(0, tk.END)
        for client in filtered_clients:
            listbox.insert(tk.END, f"{client['nombre']} {client['apellido']} - {client['email']}")

    def on_search(*args):
        query = search_var.get().lower()
        nonlocal filtered_clients
        filtered_clients = [c for c in clients if query in c['nombre'].lower() or query in c['apellido'].lower() or query in c['email'].lower()]
        refresh_list()

    search_var.trace_add('write', on_search)

    frame_form = tk.Frame(clients_win)
    frame_form.pack(fill=tk.X, padx=10, pady=10)

    tk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky="w")
    entry_nombre = tk.Entry(frame_form)
    entry_nombre.grid(row=0, column=1, sticky="ew")

    tk.Label(frame_form, text="Apellido:").grid(row=1, column=0, sticky="w")
    entry_apellido = tk.Entry(frame_form)
    entry_apellido.grid(row=1, column=1, sticky="ew")

    tk.Label(frame_form, text="Dirección:").grid(row=2, column=0, sticky="w")
    entry_direccion = tk.Entry(frame_form)
    entry_direccion.grid(row=2, column=1, sticky="ew")

    tk.Label(frame_form, text="Teléfono:").grid(row=3, column=0, sticky="w")
    entry_telefono = tk.Entry(frame_form)
    entry_telefono.grid(row=3, column=1, sticky="ew")

    tk.Label(frame_form, text="Email:").grid(row=4, column=0, sticky="w")
    entry_email = tk.Entry(frame_form)
    entry_email.grid(row=4, column=1, sticky="ew")

    profile_img_path = tk.StringVar()

    lbl_img_path = tk.Label(frame_form, text="")
    lbl_img_path.grid(row=6, column=0, columnspan=2)

    lbl_img_preview = tk.Label(clients_win)
    lbl_img_preview.pack(pady=5)

    def load_image():
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if path:
            # Crear carpeta local para imágenes si no existe
            img_dir = "imagenes_clientes"
            if not os.path.exists(img_dir):
                os.makedirs(img_dir)
            # Copiar imagen a carpeta local
            filename = os.path.basename(path)
            dest_path = os.path.join(img_dir, filename)
            shutil.copy(path, dest_path)
            profile_img_path.set(dest_path)
            lbl_img_path.config(text=dest_path)
            show_image_preview(dest_path)

    def show_image_preview(image_path):
        try:
            img = Image.open(image_path)
            img.thumbnail((150, 150))
            img_tk = ImageTk.PhotoImage(img)
            lbl_img_preview.image = img_tk
            lbl_img_preview.config(image=img_tk)
        except Exception as e:
            lbl_img_preview.config(text="No se pudo cargar la imagen")

    btn_load_img = tk.Button(frame_form, text="Cargar imagen de perfil", command=load_image)
    btn_load_img.grid(row=5, column=0, columnspan=2, pady=5)

    def clear_form():
        entry_nombre.delete(0, tk.END)
        entry_apellido.delete(0, tk.END)
        entry_direccion.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        profile_img_path.set("")
        lbl_img_path.config(text="")
        lbl_img_preview.config(image="", text="")

    def on_add():
        client = {
            "nombre": entry_nombre.get(),
            "apellido": entry_apellido.get(),
            "direccion": entry_direccion.get(),
            "telefono": entry_telefono.get(),
            "email": entry_email.get(),
            "imagen": profile_img_path.get()
        }
        if add_client(client):
            clients.append(client)
            clear_form()
            on_search()

    def on_edit():
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona un cliente para editar")
            return
        index = selected[0]
        old_client = filtered_clients[index]
        updated_client = {
            "nombre": entry_nombre.get(),
            "apellido": entry_apellido.get(),
            "direccion": entry_direccion.get(),
            "telefono": entry_telefono.get(),
            "email": entry_email.get(),
            "imagen": profile_img_path.get()
        }
        if update_client(old_client["email"], updated_client):
            clients[clients.index(old_client)] = updated_client
            clear_form()
            on_search()

    def on_delete():
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona un cliente para eliminar")
            return
        index = selected[0]
        client = filtered_clients[index]
        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar cliente {client['nombre']} {client['apellido']}?")
        if confirm:
            if delete_client(client["email"]):
                clients.remove(client)
                clear_form()
                on_search()

    def on_select(event):
        selected = listbox.curselection()
        if not selected:
            return
        index = selected[0]
        client = filtered_clients[index]
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, client["nombre"])
        entry_apellido.delete(0, tk.END)
        entry_apellido.insert(0, client["apellido"])
        entry_direccion.delete(0, tk.END)
        entry_direccion.insert(0, client["direccion"])
        entry_telefono.delete(0, tk.END)
        entry_telefono.insert(0, client["telefono"])
        entry_email.delete(0, tk.END)
        entry_email.insert(0, client["email"])
        profile_img_path.set(client.get("imagen", ""))
        lbl_img_path.config(text=profile_img_path.get())
        show_image_preview(profile_img_path.get())

    def exportar_clientes_a_csv():
        try:
            ruta_csv = filedialog.asksaveasfilename(
            title="Guardar como",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")])
            if not ruta_csv:
                           return
            ruta_json = os.path.join("BaseDatos", "clientes.json")
            with open(ruta_json, "r", encoding="utf-8") as archivo_json:
                   datos_json = json.load(archivo_json)
                   if not datos_json:
                         messagebox.showwarning("Advertencia", "No Hay Para Exportar")
                         return
            with open(ruta_csv, "w", newline="", encoding="utf-8") as archivo_csv:
                               campos = datos_json[0].keys()
                               writer = csv.DictWriter(archivo_csv, fieldnames=campos)
                               writer.writeheader()
                               writer.writerows(datos_json)
                               messagebox.showinfo("Éxito", f"Exportado correctamente a:\n{ruta_csv}")
        except Exception as e:
                               messagebox.showerror("Error", f"Ocurrió un error:\n{e}")

    listbox.bind("<<ListboxSelect>>", on_select)

    frame_form.columnconfigure(1, weight=1)

    btn_add = tk.Button(clients_win, text="Agregar Cliente", command=on_add)
    btn_add.pack(side=tk.LEFT, padx=10, pady=10)

    btn_edit = tk.Button(clients_win, text="Editar Cliente", command=on_edit)
    btn_edit.pack(side=tk.LEFT, padx=10, pady=10)

    btn_delete = tk.Button(clients_win, text="Eliminar Cliente", command=on_delete)
    btn_delete.pack(side=tk.LEFT, padx=10, pady=10)

    btn_exportar = tk.Button(clients_win, text="Exportar clientes.json a CSV", command=exportar_clientes_a_csv)
    btn_exportar.pack(side=tk.LEFT, padx=10, pady=10)

    refresh_list()

