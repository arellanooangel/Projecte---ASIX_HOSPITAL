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