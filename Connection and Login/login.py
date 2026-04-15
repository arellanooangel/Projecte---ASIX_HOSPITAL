# ------------------------------
# -- Importació de llibreries --
# ------------------------------

import tkinter as tk
from tkinter import ttk, messagebox
from auth import register_user_db, login_user_db, verify_admin_credentials

# -------------------------------------------
# -- Funció per gestionar el registre --
# -------------------------------------------

def register_user():
    """
    Obté les dades del formulari i registra un nou usuari.
    """
    username = reg_user.get().strip()
    password = reg_pass.get()
    confirm_password = reg_confirm.get()
    role = reg_role.get()

    # Validacions
    if not username or not password:
        messagebox.showerror("Error", "Cal omplir tots els camps.")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Les contrasenyes no coincideixen.")
        return

    if register_user_db(username, password, role):
        reg_user.delete(0, tk.END)
        reg_pass.delete(0, tk.END)
        reg_confirm.delete(0, tk.END)

# -------------------------------------------
# -- Funció per gestionar el login --
# -------------------------------------------

def login_user():
    """
    Gestiona l'inici de sessió dels usuaris.
    """
    username = log_user.get().strip()
    password = log_pass.get()

    role = login_user_db(username, password)

    if role:
        root.destroy()  # Tanca la finestra si el login és correcte

# -------------------------------------------
# -- Control d'accés a la pestanya de registre --
# -------------------------------------------

def on_tab_changed(event):
    """
    Quan l'usuari intenta accedir a la pestanya
    'Registrar Personal', es demanen les credencials
    de l'administrador.
    """
    selected_tab = event.widget.select()
    tab_text = event.widget.tab(selected_tab, "text")

    if tab_text == "Registrar Personal":
        if not verify_admin_credentials():
            notebook.select(login_frame)

# -------------------------------------------
# -- Configuració de la finestra principal --
# -------------------------------------------

root = tk.Tk()
root.title("UA Hospital de Blanes - Sistema d'Accés")
root.geometry("420x460")
root.resizable(False, False)
root.configure(bg="#f0f4f7")

# Estils
style = ttk.Style()
style.theme_use('default')
style.configure('TNotebook.Tab', font=('Arial', 11, 'bold'), padding=[10, 5])
style.configure('TButton', font=('Arial', 10, 'bold'))

# Títol principal
title = tk.Label(
    root,
    text="🏥 UA - Sistema d'Autenticació",
    font=("Arial", 18, "bold"),
    bg="#f0f4f7",
    fg="#2c3e50"
)
title.pack(pady=15)

# Pestanyes
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=20, pady=10)

# ------------------ LOGIN ------------------

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

ttk.Button(
    login_frame,
    text="Iniciar Sessió",
    command=login_user
).pack(pady=20)

# ---------------- REGISTER -----------------

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

ttk.Button(
    register_frame,
    text="Registrar Usuari",
    command=register_user
).pack(pady=15)

# Associar l'esdeveniment de canvi de pestanya
notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

# Peu de pàgina
footer = tk.Label(
    root,
    text="Projecte Intermodular ASIX 2025/2026 - Angel & Unai",
    bg="#f0f4f7",
    fg="gray",
    font=("Arial", 9)
)
footer.pack(pady=5)

# Execució de l'aplicació
root.mainloop()