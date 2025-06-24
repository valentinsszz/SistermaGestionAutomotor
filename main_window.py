import ttkbootstrap as ttk
import tkinter as tk
import menu
from register_window import open_register_window
from manage_users_window import open_manage_users_window
from categories_window import open_categories_window
from clientes_window import open_clients_window
from product_windows import open_product_window
from pedidos_window import abrir_ventana_pedidos
from pedidos_list_window import open_pedidos_list_window


def open_main_window(nivel_usuario):
    main_win = ttk.Window(themename="superhero")
    main_win.title("Ventana Principal")
    main_win.geometry("700x500")
    main_win.minsize(700, 500)


    def on_close_session():
        main_win.destroy()
        from main import root
        root.deiconify()

    menu.add_file_menu(main_win, on_close_session=on_close_session)

    lbl_nivel = tk.Label(main_win, text=f"Nivel de usuario: {nivel_usuario}")
    lbl_nivel.pack(pady=10)

    def on_logout():
        main_win.destroy()

    btn_logout = tk.Button(main_win, text="Salir", command=on_logout)
    btn_logout.pack(padx=20, pady=10)

    if nivel_usuario == "admin":
        btn_register = tk.Button(main_win, text="Registrar nuevo usuario", command=lambda: open_register_window(main_win))
        btn_register.pack(padx=20, pady=10)

        btn_manage_users = tk.Button(main_win, text="Gestionar usuarios", command=lambda: open_manage_users_window(main_win))
        btn_manage_users.pack(padx=20, pady=10)
        
        btn_manage_categories = tk.Button(main_win, text="Gestionar categorías", command=lambda: open_categories_window(main_win))
        btn_manage_categories.pack(padx=20, pady=10)
        
        btn_manage_product = tk.Button(main_win, text="Gestionar Productos", command=lambda: open_product_window(main_win))
        btn_manage_product.pack(padx=20, pady=10)

    if nivel_usuario == "admin" or nivel_usuario == "Vendedor":
        

        btn_manage_clients = tk.Button(main_win, text="Gestionar clientes", command=lambda: open_clients_window(main_win))
        btn_manage_clients.pack(padx=20, pady=10)

        btn_manage_pedidos = tk.Button(main_win, text="Gestionar pedidos", command=lambda: abrir_ventana_pedidos(main_win))
        btn_manage_pedidos.pack(padx=20, pady=10)

        btn_listar_pedidos = tk.Button(main_win, text="Listar pedidos", command=lambda: open_pedidos_list_window(main_win))
        btn_listar_pedidos.pack(padx=20, pady=10)
