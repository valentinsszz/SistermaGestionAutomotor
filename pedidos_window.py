import ttkbootstrap as ttk
import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

def abrir_ventana_pedidos(parent):
    win = ttk.Toplevel(parent)
    win.title("Realizar Pedido")
    win.geometry("850x650")

    # Mostrar fecha actual arriba
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
    fecha_label = ttk.Label(win, text=f"Fecha del pedido: {fecha_actual}", font=("Arial", 10, "italic"))
    fecha_label.pack(pady=5)

    # --- Cargar clientes ---
    ruta_clientes = os.path.join("BaseDatos", "clientes.json")
    if os.path.exists(ruta_clientes):
        with open(ruta_clientes, "r", encoding="utf-8") as archivo:
            clientes = json.load(archivo)
    else:
        clientes = []
    nombres_clientes = [f"{c['nombre']} {c['apellido']}" for c in clientes]

    ttk.Label(win, text="Cliente:").pack(pady=5)
    cliente_var = tk.StringVar()
    combo_clientes = ttk.Combobox(win, values=nombres_clientes, textvariable=cliente_var, state="readonly")
    combo_clientes.pack(pady=5)

    # --- Cargar categorias ---
    ruta_categorias = os.path.join("BaseDatos", "categorias.json")
    if os.path.exists(ruta_categorias):
        with open(ruta_categorias, "r", encoding="utf-8") as archivo:
            categorias = json.load(archivo)
    else:
        categorias = []


    ttk.Label(win, text="Categorias:").pack(pady=5)
    nombres_categorias = [c["name"] for c in categorias]

    categoria_var = tk.StringVar()
    combo_categorias = ttk.Combobox(win, values=nombres_categorias, textvariable=categoria_var, state="readonly")
    combo_categorias.pack(pady=5)
    if nombres_categorias:
        combo_categorias.current(0)

    # --- Cargar productos ---
    ruta_productos = os.path.join("BaseDatos", "productos.json")
    if os.path.exists(ruta_productos):
        with open(ruta_productos, "r", encoding="utf-8") as archivo:
            productos = json.load(archivo)
    else:
        productos = []

    producto_var = tk.StringVar()
    cantidad_var = tk.StringVar(value="1")

    frame_seleccion = ttk.Frame(win)
    frame_seleccion.pack(pady=10, padx=10, fill="x")

    ttk.Label(frame_seleccion, text="Producto:").grid(row=1, column=0, sticky="w")
    ttk.Label(frame_seleccion, text="Cantidad:").grid(row=1, column=2, sticky="w")
    entry_cantidad = ttk.Entry(frame_seleccion, textvariable=cantidad_var, width=5)
    entry_cantidad.grid(row=1, column=3, sticky="w", padx=5)

    def actualizar_productos():
        categoria_seleccionada = categoria_var.get()
        productos_filtrados = [p for p in productos if p.get("categoria") == categoria_seleccionada]
        nombres_productos = [p["nombre"] for p in productos_filtrados]
        combo_productos.config(values=nombres_productos)
        if nombres_productos:
            combo_productos.current(0)
        else:
            combo_productos.set("")

    combo_productos = ttk.Combobox(frame_seleccion, state="readonly", textvariable=producto_var)
    combo_productos.grid(row=1, column=1, sticky="ew", padx=5)

    
 
    actualizar_productos()

    combo_categorias.bind("<<ComboboxSelected>>", lambda e: actualizar_productos())

    boton_agregar = ttk.Button(frame_seleccion, text="Agregar")
    boton_agregar.grid(row=1, column=4, padx=10)

    # --- Treeview para mostrar productos añadidos ---
    columnas = ("Producto", "Cantidad", "Precio unitario", "Subtotal")
    tree = ttk.Treeview(win, columns=columnas, show="headings", height=10)
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.pack(padx=10, pady=10, fill="both", expand=True)

    total_var = tk.StringVar(value="Total: $0.00")
    label_total = ttk.Label(win, textvariable=total_var, font=("Arial", 14, "bold"))
    label_total.pack(pady=5)

    def actualizar_total():
        total = 0
        for child in tree.get_children():
            subtotal_str = tree.item(child)["values"][3]
            subtotal = float(subtotal_str.replace("$", ""))
            total += subtotal
        total_var.set(f"Total: ${total:.2f}")

    def agregar_producto():
        nombre = producto_var.get()
        try:
            cantidad = int(cantidad_var.get())
            if cantidad <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Cantidad inválida")
            return

        producto = next((p for p in productos if p["nombre"] == nombre), None)
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado")
            return

        subtotal = producto["precio"] * cantidad
        tree.insert("", "end", values=(nombre, cantidad, f"${producto['precio']:.2f}", f"${subtotal:.2f}"))
        actualizar_total()
        cantidad_var.set("1")

    boton_agregar.config(command=agregar_producto)

    def guardar_pedido():
        cliente = cliente_var.get()
        if not cliente:
            messagebox.showwarning("Atención", "Seleccioná un cliente")
            return
        if not tree.get_children():
            messagebox.showwarning("Atención", "No hay productos en el pedido")
            return

        productos_pedido = []
        for item in tree.get_children():
            nombre, cantidad, precio, subtotal = tree.item(item)["values"]
            productos_pedido.append({
                "producto": nombre,
                "cantidad": int(cantidad),
                "precio_unitario": precio,
                "subtotal": subtotal
            })

        pedido = {
            "cliente": cliente,
            "productos": productos_pedido,
            "total": total_var.get(),
            "fecha": fecha_actual
        }

        ruta_pedidos = os.path.join("BaseDatos", "pedidos.json")
        if os.path.exists(ruta_pedidos):
            with open(ruta_pedidos, "r", encoding="utf-8") as archivo:
                try:
                    pedidos = json.load(archivo)
                except json.JSONDecodeError:
                    pedidos = []
        else:
            pedidos = []

        # Generar id único para el pedido
        max_id = max([p.get("id", 0) for p in pedidos], default=0)
        pedido["id"] = max_id + 1

        pedidos.append(pedido)

        with open(ruta_pedidos, "w", encoding="utf-8") as archivo:
            json.dump(pedidos, archivo, indent=4, ensure_ascii=False)

        messagebox.showinfo("Éxito", "Pedido guardado correctamente")
        win.destroy()

    ttk.Button(win, text="Guardar Pedido", command=guardar_pedido).pack(pady=10)