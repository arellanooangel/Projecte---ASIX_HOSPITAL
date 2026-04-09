# ------------------------------
# -- Importació de llibreries --
# ------------------------------

import tkinter as tk  # Interfície gràfica
from tkinter import ttk, messagebox  # ttk: proporciona widgets amb disseny més modern -- messagebox: mostra missatges (error, avisos i confirmacions)
import json  # Permet guardar i llegir els usuaris en el fitxer json
import os  # S'utilitza per comprovar si l'arxiu d'usuari existeix
import hashlib  # Permet xifrar les contrasenyes mitjançant funcions hash (SHA-256)

# ------------------------------------
# -- Definició del fitxer d'usuaris --
# ------------------------------------

USER_FILE = "user.json"

# ---------------------------
# -- Funcions de seguretat --
# ---------------------------

# Funció que permet convertir la contrasenya en un hash SHA-256
# Això evita guardar contrasenyes en text pla, augmentant la seva seguretat
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Funció que permet comprovar si l'arxiu "user.json" existeix
# Si no existeix, crea un usuari per defecte
# Si ja existeix, l'obre i carrega els usuaris amb "json.load"
def load_users():
    if not os.path.exists(USER_FILE):
        default_user = {
            "admin": {
                "password": hash_password("admin123"),
                "role": "admin"
            }
        }
        save_users(default_user)
        return default_user

    with open(USER_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

# Funció que permet desar el diccionari d'usuaris a l'arxiu "user.json"
# "indent=4" millora la llegibilitat de l'arxiu
def save_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)

# ------------------------------------
# -- Funcions de registre d'usuaris --
# ------------------------------------

def register_user():
    username = reg_user.get().strip()
    password = reg_pass.get()
    confirm_password = reg_confirm.get()
    role = reg_role.get()

    # -- Validacions --

    # Verifica que tots els camps estiguin complets
    if not username or not password:
        messagebox.showerror("Error", "Cal omplir tots els camps.")
        return

    # Comprova que les 2 contrasenyes coincideixen
    if password != confirm_password:
        messagebox.showerror("Error", "Les contrasenyes no coincideixen.")
        return

    # Carrega els usuaris existents
    users = load_users()

    # Evita registrar usuaris duplicats
    if username in users:
        messagebox.showerror("Error", "L'usuari ja existeix.")
        return

    # -- Guardat de l'usuari --

    # S'afegeix el nou usuari al diccionari, la contrasenya es guarda en forma hash i es guarda l'arxiu actualitzat
    users[username] = {
        "password": hash_password(password),
        "role": role
    }

    # Desa els usuaris al fitxer
    save_users(users)

    messagebox.showinfo("Èxit", "Usuari registrat correctament.")

    # -- Neteja de camps --

    # Neteja els camps del formulari després del registre
    reg_user.delete(0, tk.END)
    reg_pass.delete(0, tk.END)
    reg_confirm.delete(0, tk.END)

# -----------------------------
# -- Funció d'inici de sessió --
# -----------------------------

def login_user():

    # -- Obtenció de credencials --
    username = log_user.get().strip()
    password = log_pass.get()

    # Carrega els usuaris existents
    users = load_users()

    # -- Verificació --

    # Comprova que l'usuari existeixi i que la contrasenya coincideixi amb el hash emmagatzemat
    if username in users and users[username]["password"] == hash_password(password):
        
        # -- Resultat de la verificació --

        # Mostra un missatge de benvinguda i tanca la finestra per continuar amb l'aplicació principal
        messagebox.showinfo(
            "Benvingut",
            f"Benvingut/da {username}!\nRol: {users[username]['role']}"
        )
        root.destroy()  # Aquí es podria obrir el menú principal
    else:
        # Error de la verificació
        messagebox.showerror("Error", "Usuari o contrasenya incorrectes.")

# -------------------------------------------
# -- Configuració de la finestra principal --
# -------------------------------------------

root = tk.Tk()
root.title("Hospital de Blanes - Sistema d'Accés")  # Títol de la finestra
root.geometry("420x420")  # Mida de la finestra
root.resizable(False, False)  # Evita que l'usuari modifiqui la mida
root.configure(bg="#f0f4f7")  # Defineix el color del fons

# ------------------------
# -- Estils amb Tkinter --
# ------------------------

# Això permet personalitzar l'aparença de les pestanyes i els botons
style = ttk.Style()
style.theme_use('default')
style.configure('TNotebook.Tab', font=('Arial', 11, 'bold'), padding=[10, 5])
style.configure('TButton', font=('Arial', 10, 'bold'))

# ---------------------
# -- Títol principal --
# ---------------------

# Títol visual
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

# Permet separar amb dues pestanyes el Login i el Registre de l'usuari
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=20, pady=10)

# -----------------------------
# -- Pestanya de LOGIN --
# -----------------------------

# Creació del contenidor
login_frame = tk.Frame(notebook, bg="white")
notebook.add(login_frame, text="Iniciar Sessió")

# Camps d'entrada
tk.Label(login_frame, text="👤 Nom d'usuari", bg="white",
         font=("Arial", 11)).pack(pady=(20, 5))

log_user = tk.Entry(login_frame, width=30, font=("Arial", 11))
log_user.pack(pady=5)

tk.Label(login_frame, text="🔒 Contrasenya", bg="white",
         font=("Arial", 11)).pack(pady=5)

log_pass = tk.Entry(login_frame, show="*", width=30, font=("Arial", 11))
log_pass.pack(pady=5)

# Botó d'inici de sessió
login_button = ttk.Button(
    login_frame,
    text="Iniciar Sessió",
    command=login_user
)
login_button.pack(pady=20)

# ---------------------------
# -- Pestanya de REGISTRE --
# ---------------------------

# Creació del contenidor
register_frame = tk.Frame(notebook, bg="white")
notebook.add(register_frame, text="Registrar Usuari")

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

# Botó de registre
register_button = ttk.Button(
    register_frame,
    text="Registrar Usuari",
    command=register_user
)
register_button.pack(pady=15)

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