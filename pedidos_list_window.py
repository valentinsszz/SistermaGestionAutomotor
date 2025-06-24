import ttkbootstrap as ttk
import tkinter as tk
from tkinter import messagebox
import json
import os

def open_pedidos_list_window(parent):
    win = ttk.Toplevel(parent)
    win.title("Listado de Pedidos")
    win.geometry("800x600")

    columnas = ("ID", "Cliente", "Fecha", "Total")
    tree = ttk.Treeview(win, columns=columnas, show="headings")
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    ruta_pedidos = os.path.join("BaseDatos", "pedidos.json")
    if os.path.exists(ruta_pedidos):
        with open(ruta_pedidos, "r", encoding="utf-8") as archivo:
            pedidos = json.load(archivo)
    else:
        pedidos = []

    def refresh_list():
        tree.delete(*tree.get_children())
        for pedido in pedidos:
            tree.insert("", "end", values=(
                pedido.get("id", ""),
                pedido.get("cliente", ""),
                pedido.get("fecha", ""),
                pedido.get("total", "")
            ))

    refresh_list()

    def on_view_details():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona un pedido para ver detalles")
            return
        item = tree.item(selected[0])
        pedido_id = item["values"][0]
        pedido = next((p for p in pedidos if p.get("id") == pedido_id), None)
        if not pedido:
            messagebox.showerror("Error", "Pedido no encontrado")
            return

        detalles = f"Cliente: {pedido.get('cliente')}\nFecha: {pedido.get('fecha')}\nTotal: {pedido.get('total')}\n\nProductos:\n"
        for prod in pedido.get("productos", []):
            detalles += f"- {prod['producto']}: {prod['cantidad']} x {prod['precio_unitario']} = {prod['subtotal']}\n"

        messagebox.showinfo(f"Detalles del Pedido {pedido_id}", detalles)

    def on_delete():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona un pedido para eliminar")
            return
        item = tree.item(selected[0])
        pedido_id = item["values"][0]
        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar pedido con ID {pedido_id}?")
        if not confirm:
            return
        nonlocal pedidos
        pedidos = [p for p in pedidos if p.get("id") != pedido_id]
        with open(ruta_pedidos, "w", encoding="utf-8") as archivo:
            json.dump(pedidos, archivo, indent=4, ensure_ascii=False)
        tree.delete(selected[0])

    def enviar_whatsapp():
        import http.client
        import json as js

        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona un pedido para enviar WhatsApp")
            return
        item = tree.item(selected[0])
        pedido_id = item["values"][0]
        pedido = next((p for p in pedidos if p.get("id") == pedido_id), None)
        if not pedido:
            messagebox.showerror("Error", "Pedido no encontrado")
            return

        # Intentar obtener teléfono del cliente desde el pedido
        telefono = None
        cliente_nombre = pedido.get("cliente", "")
        # Buscar teléfono en clientes.json
        ruta_clientes = os.path.join("BaseDatos", "clientes.json")
        if os.path.exists(ruta_clientes):
            with open(ruta_clientes, "r", encoding="utf-8") as f:
                clientes = js.load(f)
            for c in clientes:
                nombre_completo = f"{c.get('nombre', '')} {c.get('apellido', '')}"
                if nombre_completo == cliente_nombre:
                    telefono = c.get("telefono")
                    break

        if not telefono:
            messagebox.showerror("Error", "No se encontró el teléfono del cliente")
            return

        conn = http.client.HTTPConnection("api-hey.voipgroup.com")
        payload = js.dumps({
            "params": cliente_nombre,
            "destination": telefono,
            "templateid": "8206a3c7-2922-4ca3-a298-0e973aeca35f",
            "channelId": 24,
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJJZCI6IjE3OCIsIlVzZXJuYW1lIjoiaW5zaWRlLWFkbSIsIkxldmVsIjoiMyIsIkNvcnBJZCI6Ijk2IiwiUXVldWVNZW1iZXJJZCI6IjI0NiIsIm5iZiI6MTc1MDYzOTg0NSwiZXhwIjoxNzUwNjQzNDQ1LCJpYXQiOjE3NTA2Mzk4NDV9.LbTE308m1y1795N5eMFiaQFrmJuak3AeW8TqiCge0nA"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        #http://api-hey.voipgroup.com/api/v2/template/send/params/
        conn.request("POST", "/api/v2/template/send/params/", payload, headers)
        res = conn.getresponse()
        data = res.read()
        response_text = data.decode("utf-8")

        messagebox.showinfo("WhatsApp", f"Respuesta del servidor:\n{response_text}")

    btn_detalles = tk.Button(win, text="Ver Detalles", command=on_view_details)
    btn_detalles.pack(pady=10)

    btn_eliminar = tk.Button(win, text="Eliminar Pedido", command=on_delete)
    btn_eliminar.pack(pady=10)

    btn_whatsapp = tk.Button(win, text="Enviar WhatsApp", command=enviar_whatsapp)
    btn_whatsapp.pack(pady=10)

