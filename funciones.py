import json
import os

from tkinter import messagebox

#Archivos con info
PATH_FILES = "./BaseDatos/"
USERS_FILE = PATH_FILES+"usuarios.json"
CATEGORIES_FILE = PATH_FILES+"categorias.json"
CLIENTS_FILE = PATH_FILES+"clientes.json"
REMEMBERED_USER_FILE = PATH_FILES+"recordar_user.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def update_user(username, new_password, new_level):
    users = load_users()
    if username in users:
        users[username]["password"] = new_password
        users[username]["nivel"] = new_level
        save_users(users)
        return True
    return False

def login(username, password):
    users = load_users()
    if username in users and users[username]["password"] == password:
        messagebox.showinfo("Login exitoso", f"Bienvenido, {username}!")
        return users[username]["nivel"]
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        return None

def load_categories():
    if not os.path.exists(CATEGORIES_FILE):
        return []
    with open(CATEGORIES_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_categories(categories):
    with open(CATEGORIES_FILE, "w") as f:
        json.dump(categories, f)
        

def add_category(name):
    categories = load_categories()
    if any(cat["name"] == name for cat in categories):
        messagebox.showerror("Error", "La categoría ya existe")
        return False
    new_id = max([cat["id"] for cat in categories], default=0) + 1
    categories.append({"id": new_id, "name": name})
    save_categories(categories)
    messagebox.showinfo("Éxito", f"Categoría '{name}' agregada")
    return True

def update_category(old_name, new_name):
    categories = load_categories()
    if not any(cat["name"] == old_name for cat in categories):
        messagebox.showerror("Error", "La categoría no existe")
        return False
    if any(cat["name"] == new_name and cat["name"] != old_name for cat in categories):
        messagebox.showerror("Error", "La nueva categoría ya existe")
        return False
    for cat in categories:
        if cat["name"] == old_name:
            cat["name"] = new_name
            break
    save_categories(categories)
    messagebox.showinfo("Éxito", f"Categoría '{old_name}' actualizada a '{new_name}'")
    return True

def delete_category(name):
    categories = load_categories()
    if not any(cat["name"] == name for cat in categories):
        messagebox.showerror("Error", "La categoría no existe")
        return False
    categories = [cat for cat in categories if cat["name"] != name]
    save_categories(categories)
    messagebox.showinfo("Éxito", f"Categoría '{name}' eliminada")
    return True

def load_clients():
    if not os.path.exists(CLIENTS_FILE):
        return []
    with open(CLIENTS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_clients(clients):
    with open(CLIENTS_FILE, "w") as f:
        json.dump(clients, f)

def add_client(client):
    clients = load_clients()
    if any(c["email"] == client["email"] for c in clients):
        messagebox.showerror("Error", "El email del cliente ya existe")
        return False
    clients.append(client)
    save_clients(clients)
    messagebox.showinfo("Éxito", f"Cliente {client['nombre']} agregado")
    return True

def update_client(email, updated_client):
    clients = load_clients()
    for i, c in enumerate(clients):
        if c["email"] == email:
            clients[i] = updated_client
            save_clients(clients)
            messagebox.showinfo("Éxito", f"Cliente {updated_client['nombre']} actualizado")
            return True
    messagebox.showerror("Error", "Cliente no encontrado")
    return False

def delete_client(email):
    clients = load_clients()
    new_clients = [c for c in clients if c["email"] != email]
    if len(new_clients) == len(clients):
        messagebox.showerror("Error", "Cliente no encontrado")
        return False
    save_clients(new_clients)
    messagebox.showinfo("Éxito", "Cliente eliminado")
    return True



def load_remembered_user():
    if not os.path.exists(REMEMBERED_USER_FILE):
        return None, None
    with open(REMEMBERED_USER_FILE, "r") as f:
        try:
            data = json.load(f)
            return data.get("username"), data.get("password")
        except json.JSONDecodeError:
            return None, None
        
def save_remembered_user(username, password):
    data = {"username": username, "password": password}
    with open(REMEMBERED_USER_FILE, "w") as f:
        json.dump(data, f)