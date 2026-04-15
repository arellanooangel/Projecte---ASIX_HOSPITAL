import tkinter as tk
from tkinter import ttk, messagebox
from auth import register_user_db, login_user_db, verify_admin_credentials


# -------------------------------------------
# LOGIN
# -------------------------------------------

def login_user():
    username = log_user.get().strip()
    password = log_pass.get()

    role = login_user_db(username, password)

    if role:
        messagebox.showinfo("OK", f"Login correcte. Rol: {role}")
        root.destroy()
    else:
        messagebox.showerror("Error", "Usuari o contrasenya incorrectes")


# -------------------------------------------
# REGISTER
# -------------------------------------------

def register_user():
    username = reg_user.get().strip()
    password = reg_pass.get()
    confirm = reg_confirm.get()
    role = reg_role.get()

    if not username or not password:
        messagebox.showerror("Error", "Cal omplir tots els camps.")
        return

    if password != confirm:
        messagebox.showerror("Error", "Les contrasenyes no coincideixen.")
        return

    register_user_db(username, password, role)


# -------------------------------------------
# CONTROL PESTAÑA ADMIN
# -------------------------------------------

def on_tab_changed(event):
    tab = event.widget.tab(event.widget.select(), "text")

    if tab == "Registrar Personal":
        if not verify_admin_credentials():
            messagebox.showwarning(
                "Accés denegat",
                "Només administrador pot accedir."
            )
            event.widget.select(0)


# -------------------------------------------
# INTERFÍCIE (TU ORIGINAL)
# -------------------------------------------

root = tk.Tk()
root.title("UA Hospital de Blanes - Sistema d'Accés")
root.geometry("420x460")
root.resizable(False, False)
root.configure(bg="#f0f4f7")

style = ttk.Style()
style.theme_use('default')
style.configure('TNotebook.Tab', font=('Arial', 11, 'bold'), padding=[10, 5])
style.configure('TButton', font=('Arial', 10, 'bold'))

title = tk.Label(
    root,
    text="🏥 UA - Sistema d'Autenticació",
    font=("Arial", 18, "bold"),
    bg="#f0f4f7",
    fg="#2c3e50"
)
title.pack(pady=15)

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=20, pady=10)

notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

# ------------------ LOGIN ------------------

login_frame = tk.Frame(notebook, bg="white")
notebook.add(login_frame, text="Iniciar Sessió")

tk.Label(login_frame, text="👤 Nom d'usuari", bg="white").pack(pady=(20, 5))
log_user = tk.Entry(login_frame, width=30)
log_user.pack(pady=5)

tk.Label(login_frame, text="🔒 Contrasenya", bg="white").pack(pady=5)
log_pass = tk.Entry(login_frame, show="*", width=30)
log_pass.pack(pady=5)

ttk.Button(login_frame, text="Iniciar Sessió", command=login_user).pack(pady=20)


# ---------------- REGISTER -----------------

register_frame = tk.Frame(notebook, bg="white")
notebook.add(register_frame, text="Registrar Personal")

tk.Label(register_frame, text="👤 Nom d'usuari", bg="white").pack(pady=(15, 5))
reg_user = tk.Entry(register_frame, width=30)
reg_user.pack(pady=5)

tk.Label(register_frame, text="🔒 Contrasenya", bg="white").pack(pady=5)
reg_pass = tk.Entry(register_frame, show="*", width=30)
reg_pass.pack(pady=5)

tk.Label(register_frame, text="🔒 Confirmar Contrasenya", bg="white").pack(pady=5)
reg_confirm = tk.Entry(register_frame, show="*", width=30)
reg_confirm.pack(pady=5)

tk.Label(register_frame, text="👔 Rol", bg="white").pack(pady=5)
reg_role = ttk.Combobox(
    register_frame,
    values=["admin", "metge", "infermeria", "vari"],
    state="readonly",
    width=27
)
reg_role.set("metge")
reg_role.pack(pady=5)

ttk.Button(register_frame, text="Registrar Usuari", command=register_user).pack(pady=15)


# FOOTER (IGUAL)
footer = tk.Label(
    root,
    text="Projecte Intermodular ASIX 2025/2026 - Angel & Unai",
    bg="#f0f4f7",
    fg="gray",
    font=("Arial", 9)
)
footer.pack(pady=5)

root.mainloop()