# ------------------------------
# -- Importació de llibreries --
# ------------------------------

import tkinter as tk  # Interfície gràfica
from tkinter import ttk, messagebox, simpledialog  # ttk: widgets moderns; messagebox: missatges; simpledialog: entrada senzilla
import json  # Permet guardar i llegir els usuaris en fitxer JSON
import os  # Permet comprovar si l'arxiu d'usuaris existeix
import hashlib  # Xifrat de contrasenyes amb hash SHA-256

# ------------------------------------
# -- Definició del fitxer d'usuaris --
# ------------------------------------

USERS_FILE = "users.json"  # Fitxer on es guarden tots els usuaris

# ------------------------------------
# -- Contrasenya d'accés al personal --
# ------------------------------------

STAFF_ACCESS_PASSWORD = "admin123"  # Contrasenya per accedir al registre de personal

# ---------------------------
# -- Funcions de seguretat --
# ---------------------------

def hash_password(password):
    """
    Converteix una contrasenya en hash SHA-256
    Això evita guardar contrasenyes en text pla i augmenta la seguretat
    """
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """
    Comprova si el fitxer d'usuaris existeix.
    Si no existeix, crea un usuari per defecte ('admin').
    Si existeix, carrega els usuaris amb json.load.
    """
    if not os.path.exists(USERS_FILE):
        default_user = {
            "admin": {
                "password": hash_password("admin123"),
                "role": "admin"
            }
        }
        save_users(default_user)  # Desa l'usuari per defecte
        return default_user

    with open(USERS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)  # Carrega els usuaris existents
    
def save_users(users):
    """
    Desa el diccionari d'usuaris a l'arxiu JSON
    'indent=4' millora la llegibilitat
    """
    with open(USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)

# Carreguem els usuaris existents
users = load_users()

# ------------------------------------
# -- Funcions de registre d'usuaris --
# ------------------------------------

def register_user():
    """
    Registra un nou usuari amb validació de camps,
    contrasenya i rol. Desa l'usuari en el fitxer JSON.
    """
    username = reg_user.get().strip()
    password = reg_pass.get()
    confirm_password = reg_confirm.get()
    role = reg_role.get()

    # -- Validacions --

    if not username or not password:
        messagebox.showerror("Error", "Cal omplir tots els camps.")  # Error si algun camp està buit
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Les contrasenyes no coincideixen.")  # Error si les contrasenyes no coincideixen
        return

    if username in users:
        messagebox.showerror("Error", "L'usuari ja existeix.")  # Evita duplicats
        return

    # -- Guardat de l'usuari --

    users[username] = {
        "password": hash_password(password),  # Desa la contrasenya en hash
        "role": role  # Desa el rol seleccionat
    }
    save_users(users)  # Desa el fitxer actualitzat
    messagebox.showinfo("Èxit", "Usuari registrat correctament.")  # Confirmació

    # -- Neteja de camps --

    reg_user.delete(0, tk.END)
    reg_pass.delete(0, tk.END)
    reg_confirm.delete(0, tk.END)

# ------------------------------
# -- Funció d'inici de sessió --
# ------------------------------

def login_user():
    """
    Inicia sessió d'un usuari existent.
    Comprova que l'usuari i la contrasenya coincideixin.
    """
    username = log_user.get().strip()
    password = log_pass.get()

    if username in users and users[username]["password"] == hash_password(password):
        messagebox.showinfo(
            "Benvingut",
            f"Benvingut/da {username}!\nRol: {users[username]['role']}"
        )
        root.destroy()  # Tanca la finestra de login
    else:
        messagebox.showerror("Error", "Usuari o contrasenya incorrectes.")  # Error si falla el login

# ----------------------------------------------
# -- Funcions d'accés al registre de personal --
# ----------------------------------------------

def verify_staff_access(event):
    """
    Demana la contrasenya d'administrador per accedir
    al registre de personal.
    """
    password = simpledialog.askstring(
        "Accés restringit",
        "Introdueix la contrasenya d'administrador:",
        show="*"
    )

    if password is None:  # Si l'usuari prem Cancel·lar
        notebook.select(login_frame)
        return

    if password != STAFF_ACCESS_PASSWORD:
        messagebox.showerror("Accés denegat", "Contrasenya incorrecta.")  # Error si la contrasenya no és correcta
        notebook.select(login_frame)
    else:
        messagebox.showinfo("Accés concedit", "Pots registrar nou personal.")  # Accés concedit

def on_tab_changed(event):
    """
    Detecta quan es canvia de pestanya i comprova
    l'accés a la pestanya de registre de personal.
    """
    selected_tab = event.widget.select()
    tab_text = event.widget.tab(selected_tab, "text")
    if tab_text == "Registrar Personal":
        verify_staff_access(event)

# -------------------------------------------
# -- Configuració de la finestra principal --
# -------------------------------------------

root = tk.Tk()
root.title("Hospital de Blanes - Sistema d'Accés")
root.geometry("420x450")
root.resizable(False, False)
root.configure(bg="#f0f4f7")

# ------------------------
# -- Estils amb Tkinter --
# ------------------------

style = ttk.Style()
style.theme_use('default')
style.configure('TNotebook.Tab', font=('Arial', 11, 'bold'), padding=[10, 5])
style.configure('TButton', font=('Arial', 10, 'bold'))

# ---------------------
# -- Titol principal --
# ---------------------

title = tk.Label(
    root,
    text="🏥 Sistema d'Autenticació",
    font=("Arial", 18, "bold"),
    bg="#f0f4f7",
    fg="#2c3e50"
)
title.pack(pady=15)

# ---------------
# -- Pestanyes --
# ---------------

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=20, pady=10)

# -- Pestanya de login --
login_frame = tk.Frame(notebook, bg="white")
notebook.add(login_frame, text="Iniciar Sessió")

tk.Label(login_frame, text="👤 Nom d'usuari", bg="white",
         font=("Arial", 11)).pack(pady=(20, 5))
log_user = tk.Entry(login_frame, width=30, font=("Arial", 11))
log_user.pack(pady=5)

tk.Label(login_frame, text="🔒 Contrasenya", bg="white",
         font=("Arial", 11)).pack(pady=5)
log_pass = tk.Entry(login_frame, show="*", width=30, font=("Arial", 11))
log_pass.pack(pady=5)

login_button = ttk.Button(
    login_frame,
    text="Iniciar Sessió",
    command=login_user
)
login_button.pack(pady=20)

# -- Pestanya de registre --
register_frame = tk.Frame(notebook, bg="white")
notebook.add(register_frame, text="Registrar Personal")

tk.Label(register_frame, text="👤 Nom d'usuari", bg="white",
         font=("Arial", 11)).pack(pady=(15, 5))
reg_user = tk.Entry(register_frame, width=30, font=("Arial", 11))
reg_user.pack(pady=5)

tk.Label(register_frame, text="🔒 Contrasenya", bg="white",
         font=("Arial", 11)).pack(pady=5)
reg_pass = tk.Entry(register_frame, show="*", width=30, font=("Arial", 11))
reg_pass.pack(pady=5)

tk.Label(register_frame, text="🔒 Confirmar Contrasenya", bg="white",
         font=("Arial", 11)).pack(pady=5)
reg_confirm = tk.Entry(register_frame, show="*", width=30, font=("Arial", 11))
reg_confirm.pack(pady=5)

tk.Label(register_frame, text="👔 Rol", bg="white",
         font=("Arial", 11)).pack(pady=5)
reg_role = ttk.Combobox(
    register_frame,
    values=["admin", "metge", "infermeria", "administratiu"],
    state="readonly",
    width=27
)
reg_role.set("metge")
reg_role.pack(pady=5)

register_button = ttk.Button(
    register_frame,
    text="Registrar Usuari",
    command=register_user
)
register_button.pack(pady=15)

# -- Associem l'esdeveniment de canvi de pestanya --
notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

# -------------------
# -- Peu de pàgina --
# -------------------

footer = tk.Label(
    root,
    text="Projecte Intermodular ASIX 2025/2026 - Angel & Unai",
    bg="#f0f4f7",
    fg="gray",
    font=("Arial", 9)
)
footer.pack(pady=5)

# -----------------------------
# -- Execució de l'aplicació --
# -----------------------------

root.mainloop()