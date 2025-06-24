import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
import json
import os
import shutil


from tkinter import filedialog
from PIL import Image, ImageTk

# Rutas a los archivos
RUTA_CATEGORIAS = "BaseDatos/categorias.json"
RUTA_PRODUCTOS = "BaseDatos/productos.json"

# Funciones de archivo
def load_categories():
    if not os.path.exists(RUTA_CATEGORIAS):
        return []
    with open(RUTA_CATEGORIAS, "r", encoding="utf-8") as file:
        data = json.load(file)
        return [cat["name"] for cat in data]
    
    

def load_product():
    if not os.path.exists(RUTA_PRODUCTOS):
        return []
    with open(RUTA_PRODUCTOS, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except:
            return []

def save_product(productos):
    with open(RUTA_PRODUCTOS, "w", encoding="utf-8") as file:
        json.dump(productos, file, indent=4, ensure_ascii=False)

# Función principal
def open_product_window(parent):
    prod_win = ttk.Toplevel(parent)
    prod_win.title("Gestión de Productos")
    prod_win.geometry("850x850+200+50")
    prod_win.minsize(850, 850)
    

    ttk.Label(prod_win, text="Nombre:").pack()
    entry_nombre = ttk.Entry(prod_win)
    entry_nombre.pack()

    ttk.Label(prod_win, text="Precio:").pack()
    entry_precio = ttk.Entry(prod_win)
    entry_precio.pack()

    ttk.Label(prod_win, text="Categoría:").pack()
    categorias = load_categories()
    combo_categoria = ttk.Combobox(prod_win, values=categorias, state="readonly")
    combo_categoria.pack()

    ruta_imagen = tk.StringVar()
    def cargar_imagen():
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen", 
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.gif")]
        )
        if ruta:
            img_dir = "imagenes_productos"
            os.makedirs(img_dir, exist_ok=True)
            filename = os.path.basename(ruta)
            ruta_dest = os.path.join(img_dir, filename)
            if not os.path.exists(ruta_dest):
                shutil.copy(ruta, ruta_dest)
            ruta_imagen.set(ruta_dest)
            mostrar_imagen(ruta_dest)

    def mostrar_imagen(ruta):
        try:
            img=Image.open(ruta)
            img.thumbnail((150,150))
            img_tk=ImageTk.PhotoImage(img)
            label_imagen.config(image=img_tk)
            label_imagen.image=img_tk
        except:
            label_imagen.config(text="Error al cargar la imagen")


    ttk.Button(prod_win, text="Cargar Imagen", command=cargar_imagen).pack(padx=10, pady=10, ipadx=10, ipady=5)
    ttk.Label(prod_win, textvariable=ruta_imagen).pack()
    frame_imagen = tk.Frame(prod_win, width=150, height=150)
    frame_imagen.pack(pady=10)
    frame_imagen.pack_propagate(False)

    label_imagen = tk.Label(frame_imagen)
    label_imagen.pack(expand=True)

    columnas = ("Nombre", "Precio", "Categoría")
    tree = ttk.Treeview(prod_win, columns=columnas, show="headings")
    for col in columnas:
        tree.heading(col, text=col.capitalize())
    tree.pack(fill=tk.BOTH, expand=True, pady=10)

    def refresh_list():
        for item in tree.get_children():
            tree.delete(item)
        productos = load_product()
        for idx, p in enumerate(productos):
            tree.insert("", "end", iid=idx, values=(p["nombre"], p["precio"], p["categoria"]))

    def validarCampos():
        nombre = entry_nombre.get().strip()
        precio_str = entry_precio.get().strip()
        categoria = combo_categoria.get().strip()
        if not nombre or not precio_str or not categoria:
            messagebox.showerror("Error", "Complete todos los campos")
            return None
        try:
            precio = float(precio_str)
            if precio <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Precio inválido")
            return None
        return {"nombre": nombre, "precio": precio, "categoria": categoria, "imagen":ruta_imagen.get()}

    # Agregar producto
    def add_product():
        producto = validarCampos()
        if producto is None:
            return
        productos = load_product()
        productos.append(producto)
        save_product(productos)
        refresh_list()
        messagebox.showinfo("Éxito", "Producto agregado")

    # Eliminar producto
    def delete_product():
        seleccionado = tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Selecciona un producto para eliminar")
            return
        idx = int(seleccionado[0])
        productos = load_product()
        productos.pop(idx)
        save_product(productos)
        refresh_list()
        messagebox.showinfo("Éxito", "Producto eliminado")

    # Editar producto
    def edit_product():
        seleccionado = tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Selecciona un producto para editar")
            return
        idx = int(seleccionado[0])
        producto = validarCampos()
        if producto is None:
            return
        productos = load_product()
        productos[idx] = producto
        save_product(productos)
        refresh_list()
        messagebox.showinfo("Éxito", "Producto editado")

    # Cargar datos al hacer clic en el Tree
    def cargar_para_editar(event):
        seleccionado = tree.selection()
        if not seleccionado:
            return
        idx = int(seleccionado[0])
        productos = load_product()
        p = productos[idx]
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, p["nombre"])
        entry_precio.delete(0, tk.END)
        entry_precio.insert(0, str(p["precio"]))
        combo_categoria.set(p["categoria"])
        ruta_imagen.set(p.get("imagen", ""))
        mostrar_imagen(ruta_imagen.get())

    tree.bind("<<TreeviewSelect>>", cargar_para_editar)

    # Botones
    frame_botones = ttk.Frame(prod_win)
    frame_botones.pack(pady=10)

    ttk.Button(frame_botones, text="Agregar", command=add_product).grid(row=0, column=0, padx=5)
    ttk.Button(frame_botones, text="Editar", command=edit_product).grid(row=0, column=1, padx=5)
    ttk.Button(frame_botones, text="Eliminar", command=delete_product).grid(row=0, column=2, padx=5)

    # Mostrar productos
    refresh_list()
