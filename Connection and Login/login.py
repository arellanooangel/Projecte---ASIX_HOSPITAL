import tkinter as tk
from tkinter import ttk, messagebox
# Asumiendo que 'auth.py' contiene las funciones de conexión que vimos antes
from auth import register_personal_db, login_user_db, verify_admin_credentials

def login_user():
    u, p = log_user.get().strip(), log_pass.get()
    # login_user_db ahora debería devolver el rol o 'admin' si el login es correcto
    user_info = login_user_db(u, p) 
    
    if user_info:
        # user_info es una tupla: (username, nom, cognom1)
        messagebox.showinfo("Sistema UA", f"Login correcte.\nBenvingut/da: {user_info[1]} {user_info[2]}")
    else:
        messagebox.showerror("Error", "Usuari o contrasenya incorrectes o compte inactiu.")

def register_user():
    # Recollida de dades segons el teu SQL
    d, n, c1, c2, em = reg_dni.get().strip(), reg_nom.get().strip(), \
                       reg_c1.get().strip(), reg_c2.get().strip(), reg_email.get().strip()
    u, p = reg_user.get().strip(), reg_pass.get()
    role = reg_role.get()

    if not d or not n or not u or not p or not em:
        messagebox.showerror("Error", "Els camps amb (*) són obligatoris.")
        return

    # Enviem dades a la base de dades
    # Aquesta funció ha de gestionar la inserció en 'personal', 'usuaris' i la taula del 'rol'
    if register_personal_db(d, n, c1, c2, em, u, p, role):
        messagebox.showinfo("Èxit", f"Personal registrat correctament a la taula: {role.upper()}")
        # Neteja de camps
        for entry in [reg_dni, reg_nom, reg_c1, reg_c2, reg_email, reg_user, reg_pass]:
            entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "No s'ha pogut registrar. Revisa si el DNI o l'Usuari ja existeixen.")

def on_tab_changed(event):
    tab = event.widget.tab(event.widget.select(), "text")
    if tab == "Registrar Personal":
        # Nota: Aquesta funció hauria de comprovar si l'usuari actual loguejat és 'ua-admin'
        if not verify_admin_credentials():
            messagebox.showwarning("Accés Denegat", "Només l'administrador pot crear nou personal.")
            event.widget.select(0)

# --- CONFIGURACIÓ DE LA FINESTRA ---
root = tk.Tk()
root.title("UA Hospital - Gestió de Personal")
root.geometry("450x650")
root.resizable(False, False)
root.configure(bg="#f0f4f7")

# Estils
style = ttk.Style()
style.theme_use('clam') # Millor aspecte en sistemes moderns
style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'), padding=[10, 5])
style.configure('TButton', font=('Arial', 10, 'bold'))

tk.Label(root, text="🏥 UA - Gestió Hospitalària", font=("Arial", 16, "bold"), 
         bg="#f0f4f7", fg="#2c3e50").pack(pady=15)

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=20, pady=5)
notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

# --- PESTANYA LOGIN ---
f_log = tk.Frame(notebook, bg="white")
notebook.add(f_log, text="Iniciar Sessió")

tk.Label(f_log, text="👤 Nom d'Usuari", bg="white", font=("Arial", 9)).pack(pady=(40, 5))
log_user = tk.Entry(f_log, width=30, justify='center'); log_user.pack()

tk.Label(f_log, text="🔒 Contrasenya", bg="white", font=("Arial", 9)).pack(pady=(15, 5))
log_pass = tk.Entry(f_log, show="*", width=30, justify='center'); log_pass.pack()

ttk.Button(f_log, text="Entrar al Sistema", command=login_user).pack(pady=40)

# --- PESTANYA REGISTRE ---
f_reg = tk.Frame(notebook, bg="white")
notebook.add(f_reg, text="Registrar Personal")

# Formulari Dades Personals (Basat en la taula 'personal')
fields = [("DNI*", "reg_dni"), ("Nom*", "reg_nom"), ("Primer Cognom*", "reg_c1"), 
          ("Segon Cognom", "reg_c2"), ("Email*", "reg_email")]

for lbl, var_name in fields:
    tk.Label(f_reg, text=lbl, bg="white", font=("Arial", 8)).pack(pady=(4,0))
    en = tk.Entry(f_reg, width=35)
    en.pack()
    globals()[var_name] = en 

# Selecció de Rol (Correspon a les taules: metge, infermer, vari)
tk.Label(f_reg, text="👔 Rol / Destinació*", bg="white", font=("Arial", 8, "bold")).pack(pady=(10,0))
reg_role = ttk.Combobox(f_reg, values=["metge", "infermer", "vari"], state="readonly", width=32)
reg_role.set("metge")
reg_role.pack(pady=5)

# Separador visual
tk.Frame(f_reg, height=1, bg="#dee2e6").pack(fill="x", padx=40, pady=10)

# Dades de la taula 'usuaris'
tk.Label(f_reg, text="👤 Username*", bg="white", font=("Arial", 8)).pack()
reg_user = tk.Entry(f_reg, width=35); reg_user.pack()

tk.Label(f_reg, text="🔒 Password*", bg="white", font=("Arial", 8)).pack()
reg_pass = tk.Entry(f_reg, show="*", width=35); reg_pass.pack()

ttk.Button(f_reg, text="Registrar a la DB", command=register_user).pack(pady=20)

# Footer
tk.Label(root, text="Base de Dades: PostgreSQL | Projecte ASIX 2026", bg="#f0f4f7", 
         fg="gray", font=("Arial", 7)).pack(pady=5)

root.mainloop()