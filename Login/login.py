# ------------------------------
# -- Importació de llibreries --
# ------------------------------

import tkinter as tk # Interfície gràfica
from tkinter import ttk, messagebox # ttk: proporciona widgets amb diseny mes modern -- messagebox: mostra missatges (error, avisos i confirmacions)
import json # Permet guardar i llegir els usuaris en el fitxer json
import os # S'utilitza per comprobar si l'arxiu d'usuari existeix
import hashlib # Permet xifrar les contrasenyes mitjançant funcions hash (SHA-256)

# ------------------------------------
# -- Definició del fitxer d'usuaris --
# ------------------------------------

USER_FILE = "user.json"

# ---------------------------
# -- Funcions de seguretat --
# ---------------------------

# Funció que permet convertir la contrasenya en un hash SHA-256
# Això evita guardar contrasenyes en text pla, aumentando su seguridad
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Funció que permet comprobar si l'arxiu "user.json" existeix
# Si no existeix, crea un usuari per defecte
# Si ja existeix, ho obra y carga els arxius amb "json.load"
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
    
# Funció que permet desar el diccionari d'usuaris a l'arxiu "users.json"
# "indent=4" millora la llegibilitat de l'arxiu
def save_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)

# ------------------------------------
# -- Funcions de registre d'usuaris --
# ------------------------------------

def register_users():
    username = reg_user.get().strip()
    password = reg_pass.get()
    confirm_password = reg_confirm.get()
    role = reg_role.get()


    # -----------------
    # -- Validacions --
    # -----------------

    # Verifica que tots els camps esten complets
    if not username or not password:
        messagebox.showerror("Error", "Cal omplir tots els camps.")
    
    # Comproba que les 2 contrasenyes coincideixen
    if password != confirm_password:
        messagebox.showerror("Error", "Les contrasenyes no coincideixen.")

    # Evita registrar usuaris duplicats
    if username in users:
        messagebox.showerror("Error", "L'usuari ja existeix.")
    

    # -------------------------
    # -- Guardat de l'usuari --
    # -------------------------
    users[username] = {
        "password": hash_password(password),
        "role": role
    }


    # ---------------------
    # -- Neteja de camps --
    # ---------------------

    # Neteja els camps del formulari després del registre
    reg_user.delete(0, tk.END)
    reg_pass.delete(0, tk.END)
    reg_confirm.delete(0, tk.END)


# -----------------------------
# -- Funció d'inci de sessió --
# -----------------------------
def login_user():
