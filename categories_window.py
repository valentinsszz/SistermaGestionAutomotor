import ttkbootstrap as ttk
import tkinter as tk

from tkinter import messagebox, simpledialog
from tkinter import BOTH, END
from funciones import load_categories, add_category, update_category, delete_category

def open_categories_window(parent):
    cat_win = ttk.Toplevel(parent)
    cat_win.title("Gestionar Categorías")
    cat_win.geometry("700x500")

    categories = load_categories()

    lbl_info = tk.Label(cat_win, text="Categorías registradas:")
    lbl_info.pack(pady=5)

    listbox = tk.Listbox(cat_win)
    listbox.pack(fill=BOTH, expand=True, padx=10, pady=5)

    def refresh_list():
        listbox.delete(0, END)
        for cat in categories:
            listbox.insert(END, f"{cat['id']} - {cat['name']}")

    refresh_list()

    def add_new_category():
        new_cat = simpledialog.askstring("Nueva categoría", "Nombre de la nueva categoría:")
        if new_cat:
            if add_category(new_cat):
                categories.append({"id": max([cat["id"] for cat in categories], default=0) + 1, "name": new_cat})
                refresh_list()

    def edit_category():
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona una categoría para editar")
            return
        index = selected[0]
        old_name = categories[index]["name"]

        # Nueva ventana para editar categoría
        edit_win = tk.Toplevel(cat_win)
        edit_win.title(f"Editar categoría: {old_name}")
        edit_win.geometry("300x150")
        edit_win.grab_set()

        tk.Label(edit_win, text="Nuevo nombre:").pack(pady=5)
        entry_name = tk.Entry(edit_win)
        entry_name.pack(pady=5)
        entry_name.insert(0, old_name)

        def save_changes():
            new_name = entry_name.get()
            if not new_name:
                messagebox.showerror("Error", "El nombre no puede estar vacío")
                return
            if update_category(old_name, new_name):
                categories[index]["name"] = new_name
                refresh_list()
                edit_win.destroy()

        btn_save = tk.Button(edit_win, text="Guardar cambios", command=save_changes)
        btn_save.pack(pady=10)

    def delete_category_action():
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona una categoría para eliminar")
            return
        index = selected[0]
        name = categories[index]["name"]

        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar categoría '{name}'?")
        if confirm:
            if delete_category(name):
                categories.pop(index)
                refresh_list()

    btn_add = tk.Button(cat_win, text="Agregar categoría", command=add_new_category)
    btn_add.pack(side=tk.LEFT, padx=10, pady=10)

    btn_edit = tk.Button(cat_win, text="Editar categoría", command=edit_category)
    btn_edit.pack(side=tk.LEFT, padx=10, pady=10)

    btn_delete = tk.Button(cat_win, text="Eliminar categoría", command=delete_category_action)
    btn_delete.pack(side=tk.LEFT, padx=10, pady=10)


