import tkinter as tk
from tkinter import ttk, messagebox
from auth import register_personal_db, login_user_db, verify_admin_credentials

def login_user():
    u, p = log_user.get().strip(), log_pass.get()
    role = login_user_db(u, p)
    if role:
        messagebox.showinfo("Sistema UA", f"Login correcte.\nBenvingut/da: {u}\nRol: {role.upper()}")
    else:
        messagebox.showerror("Error", "Usuari o contrasenya incorrectes.")

def register_user():
    # Recollida de totes les dades del formulari
    d, n, c1, c2, em = reg_dni.get().strip(), reg_nom.get().strip(), \
                       reg_c1.get().strip(), reg_c2.get().strip(), reg_email.get().strip()
    u, p = reg_user.get().strip(), reg_pass.get()
    role = reg_role.get()

    if not d or not n or not u or not p:
        messagebox.showerror("Error", "Els camps amb (*) són obligatoris.")
        return

    # Enviem els 8 paràmetres (Dades personals + Accés + Rol)
    if register_personal_db(d, n, c1, c2, em, u, p, role):
        messagebox.showinfo("Èxit", f"Personal registrat correctament com a {role.upper()}")
        # Neteja de camps
        for entry in [reg_dni, reg_nom, reg_c1, reg_c2, reg_email, reg_user, reg_pass]:
            entry.delete(0, tk.END)

def on_tab_changed(event):
    tab = event.widget.tab(event.widget.select(), "text")
    if tab == "Registrar Personal":
        if not verify_admin_credentials():
            messagebox.showwarning("Accés Denegat", "Cal ser administrador per registrar nou personal.")
            event.widget.select(0)

# --- CONFIGURACIÓ DE LA FINESTRA ---
root = tk.Tk()
root.title("UA Hospital de Blanes - Gestió")
root.geometry("420x600")
root.resizable(False, False)
root.configure(bg="#f0f4f7")

# Estils
style = ttk.Style()
style.theme_use('default')
style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'), padding=[10, 5])
style.configure('TButton', font=('Arial', 10, 'bold'))

tk.Label(root, text="🏥 UA - Sistema d'Autenticació", font=("Arial", 16, "bold"), 
         bg="#f0f4f7", fg="#2c3e50").pack(pady=15)

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=20, pady=5)
notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

# --- PESTANYA LOGIN ---
f_log = tk.Frame(notebook, bg="white")
notebook.add(f_log, text="Iniciar Sessió")

tk.Label(f_log, text="👤 Usuari", bg="white").pack(pady=(30, 5))
log_user = tk.Entry(f_log, width=30); log_user.pack()

tk.Label(f_log, text="🔒 Contrasenya", bg="white").pack(pady=(15, 5))
log_pass = tk.Entry(f_log, show="*", width=30); log_pass.pack()

ttk.Button(f_log, text="Entrar al Sistema", command=login_user).pack(pady=30)

# --- PESTANYA REGISTRE ---
f_reg = tk.Frame(notebook, bg="white")
notebook.add(f_reg, text="Registrar Personal")

# Formulari Dades Personals
fields = [("DNI*", "reg_dni"), ("Nom*", "reg_nom"), ("Primer Cognom*", "reg_c1"), 
          ("Segon Cognom", "reg_c2"), ("Email*", "reg_email")]

for lbl, var_name in fields:
    tk.Label(f_reg, text=lbl, bg="white", font=("Arial", 8)).pack(pady=(5,0))
    en = tk.Entry(f_reg, width=30)
    en.pack()
    globals()[var_name] = en # Crea reg_dni, reg_nom, etc.

# Selecció de Rol / Taula
tk.Label(f_reg, text="👔 Rol de Personal*", bg="white", font=("Arial", 8, "bold")).pack(pady=(10,0))
reg_role = ttk.Combobox(f_reg, values=["metge", "infermer", "vari"], state="readonly", width=27)
reg_role.set("metge")
reg_role.pack(pady=5)

# Secció de Compte (Separador visual)
tk.Frame(f_reg, height=1, bg="#dee2e6").pack(fill="x", padx=30, pady=10)

tk.Label(f_reg, text="👤 Nou Usuari de Sistema*", bg="white").pack()
reg_user = tk.Entry(f_reg, width=30); reg_user.pack()

tk.Label(f_reg, text="🔒 Contrasenya d'Accés*", bg="white").pack()
reg_pass = tk.Entry(f_reg, show="*", width=30); reg_pass.pack()

ttk.Button(f_reg, text="Completar Registre", command=register_user).pack(pady=20)

# Footer
tk.Label(root, text="Projecte ASIX 2025/2026 - Angel & Unai", bg="#f0f4f7", 
         fg="gray", font=("Arial", 8)).pack(pady=5)

root.mainloop()