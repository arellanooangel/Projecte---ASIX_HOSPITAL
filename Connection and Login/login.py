# --------------------------
# Importació llibreries
# --------------------------
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import hashlib

from db_connexio import get_connection


# ------------------------------
# CONTRASENYA ACCÉS PERSONAL
# ------------------------------

STAFF_ACCESS_PASSWORD = "admin123"


# ---------------------------
# XIFRAR CONTRASENYA
# ---------------------------

def hash_password(password):
    """
    Converteix la contrasenya en SHA-256
    """
    return hashlib.sha256(password.encode()).hexdigest()


# ------------------------------
# REGISTRE USUARI (POSTGRESQL)
# ------------------------------

def register_user():
    """
    Registra un usuari a la base de dades PostgreSQL
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
    # Connexió a la BD
    connection = get_connection()

    if not connection:
        messagebox.showerror("Error", "No es pot connectar a la base de dades.")
        return

    try:
        cursor = connection.cursor()

        # comprovar si existeix usuari
        cursor.execute(
            "SELECT username FROM usuaris WHERE username=%s",
            (username,)
        )

        if cursor.fetchone():
            messagebox.showerror("Error", "L'usuari ja existeix.")
            return

        # inserir usuari (amb contransenya xifrada)
        cursor.execute("""
            INSERT INTO usuaris (username, password, role)
            VALUES (%s, %s, %s)
        """, (
            username,
            hash_password(password),
            role
        ))

        connection.commit()

        messagebox.showinfo("Èxit", "Usuari registrat correctament.")

        # neteja camps
        reg_user.delete(0, tk.END)
        reg_pass.delete(0, tk.END)
        reg_confirm.delete(0, tk.END)

    # Missatge error
    except Exception as e:
        messagebox.showerror("Error", f"Error registre: {e}")

    # Missatge tancament de connexió
    finally:
        cursor.close()
        connection.close()


# ------------------------------
# LOGIN USUARI (POSTGRESQL)
# ------------------------------

def login_user():
    """
    Inicia sessió amb PostgreSQL
    """

    username = log_user.get().strip()
    password = log_pass.get()

    connection = get_connection()

    if not connection:
        messagebox.showerror("Error", "No es pot connectar a la base de dades.")
        return

    try:
        cursor = connection.cursor()
        # Consulta a la BD per verificar que coincideixin
        cursor.execute("""
            SELECT role 
            FROM usuaris
            WHERE username=%s AND password=%s
        """, (
            username,
            hash_password(password)
        ))

        result = cursor.fetchone()

        if result:
            role = result[0]

            messagebox.showinfo(
                "Benvingut",
                f"Benvingut/da {username}!\nRol: {role}"
            )
            # Si existeix la coincidencia de la contrasenya tanca l'aplicació
            root.destroy()

        else:
            messagebox.showerror("Error", "Usuari o contrasenya incorrectes.")

    except Exception as e:
        messagebox.showerror("Error", f"Error login: {e}")

    finally:
        cursor.close()
        connection.close()


# ------------------------------
# CONTROL ACCÉS REGISTRE
# ------------------------------

def verify_staff_access(event):
    """
    Demana contrasenya admin per accedir al registre
    """

    password = simpledialog.askstring(
        "Accés restringit",
        "Introdueix la contrasenya d'administrador:",
        show="*"
    )

    if password is None:
        notebook.select(login_frame)
        return

    if password != STAFF_ACCESS_PASSWORD:
        messagebox.showerror("Accés denegat", "Contrasenya incorrecta.")
        notebook.select(login_frame)
    else:
        messagebox.showinfo("Accés concedit", "Pots registrar nou personal.")

# Detecta quan l'usuari canvia de pestanya en el Notebook, si intenta accedir a "Registrar Personal" s'executa la verificació d'accés
def on_tab_changed(event):
    selected_tab = event.widget.select()
    tab_text = event.widget.tab(selected_tab, "text")

    if tab_text == "Registrar Personal":
        verify_staff_access(event)


# ------------------------------
# INTERFÍCIE GRÀFICA
# ------------------------------

root = tk.Tk()
root.title("Hospital de Blanes - Sistema d'Accés")
root.geometry("420x450")
root.resizable(False, False)
root.configure(bg="#f0f4f7")

# Estils
style = ttk.Style()
style.theme_use('default')
style.configure('TNotebook.Tab', font=('Arial', 11, 'bold'), padding=[10, 5])
style.configure('TButton', font=('Arial', 10, 'bold'))

# Titol (capçalera de l'aplicació)
title = tk.Label(
    root,
    text="🏥 Sistema d'Autenticació",
    font=("Arial", 18, "bold"),
    bg="#f0f4f7",
    fg="#2c3e50"
)
title.pack(pady=15)

# Pestanyes Notebook (permeteix dividir l'interfície en dos pestanyes)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=20, pady=10)


# ---------------- LOGIN ----------------

login_frame = tk.Frame(notebook, bg="white")
notebook.add(login_frame, text="Iniciar Sessió")

tk.Label(login_frame, text="👤 Nom d'usuari", bg="white").pack(pady=(20, 5))
log_user = tk.Entry(login_frame, width=30)
log_user.pack()

tk.Label(login_frame, text="🔒 Contrasenya", bg="white").pack(pady=5)
log_pass = tk.Entry(login_frame, show="*", width=30)
log_pass.pack()

tk.Button(login_frame, text="Iniciar Sessió", command=login_user).pack(pady=20)


# ---------------- REGISTER ----------------

register_frame = tk.Frame(notebook, bg="white")
notebook.add(register_frame, text="Registrar Personal")

tk.Label(register_frame, text="👤 Nom d'usuari", bg="white").pack(pady=(15, 5))
reg_user = tk.Entry(register_frame, width=30)
reg_user.pack()

tk.Label(register_frame, text="🔒 Contrasenya", bg="white").pack(pady=5)
reg_pass = tk.Entry(register_frame, show="*", width=30)
reg_pass.pack()

tk.Label(register_frame, text="🔒 Confirmar Contrasenya", bg="white").pack(pady=5)
reg_confirm = tk.Entry(register_frame, show="*", width=30)
reg_confirm.pack()

tk.Label(register_frame, text="👔 Rol", bg="white").pack(pady=5)
reg_role = ttk.Combobox(
    register_frame,
    values=["admin", "metge", "infermeria", "administratiu"],
    state="readonly",
    width=27
)
reg_role.set("metge")
reg_role.pack()

tk.Button(register_frame, text="Registrar Usuari", command=register_user).pack(pady=15)

# Canvi de pestanya
notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

# Crea un footer informatiu en la part inferior de la interfície gràfica
footer = tk.Label(
    root,
    text="Projecte Intermodular ASIX 2025/2026 - Angel & Unai✨",
    bg="#f0f4f7",
    fg="gray",
    font=("Arial", 9)
)
footer.pack(pady=5)

# ---------------- EXECUCIÓ DE L'APLICACIÓ ----------------
root.mainloop()