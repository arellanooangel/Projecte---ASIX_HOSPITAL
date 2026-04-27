import tkinter as tk
from tkinter import ttk, messagebox
# Importació de les funcions lògiques des del fitxer extern 'auth_ok.py'
from auth_ok import (register_personal_db, login_user_db, verify_admin_credentials, insertar_pacient_db)

# ============================================================
# FUNCIONS DE LÒGICA (CONTROLADORS)
# ============================================================

def login_user():
    """Gestiona l'entrada de l'usuari al sistema."""
    u, p = log_user.get().strip(), log_pass.get()
    # Verifica credencials consultant la base de dades
    user_info = login_user_db(u, p) 
    if user_info:
        messagebox.showinfo("Sistema UA", f"Login correcte.\nBenvingut/da: {user_info[1]} {user_info[2]}")
    else:
        messagebox.showerror("Error", "Usuari o contrasenya incorrectes o compte inactiu.")

def register_user():
    """Recull les dades dels camps d'entrada i registra nou personal."""
    # Obtenim els valors eliminant espais en blanc innecessaris
    d, n, c1, c2, em = reg_dni.get().strip(), reg_nom.get().strip(), \
                       reg_c1.get().strip(), reg_c2.get().strip(), reg_email.get().strip()
    u, p = reg_user.get().strip(), reg_pass.get()
    role = reg_role.get()

    # Validació: Comprova que els camps obligatoris no estiguin buits
    if not d or not n or not u or not p or not em:
        messagebox.showerror("Error", "Els camps amb (*) són obligatoris.")
        return

    # Intenta fer la inserció a la BD
    if register_personal_db(d, n, c1, c2, em, u, p, role):
        messagebox.showinfo("Èxit", f"Personal registrat correctament a: {role.upper()}")
        # Netaja de camps després d'un registre correcte
        for entry in [reg_dni, reg_nom, reg_c1, reg_c2, reg_email, reg_user, reg_pass]:
            entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "No s'ha pogut registrar (DNI o Usuari duplicat).")

def obrir_alta_pacient():
    """Crea una finestra emergent (Toplevel) per a l'alta de pacients (Apartat 3.2)."""
    f = tk.Toplevel(); f.title("3.2 Alta de Pacient"); f.geometry("300x350")
    
    # Disseny del formulari d'alta de pacients
    tk.Label(f, text="Targeta Sanitària:").pack(pady=5)
    ts = tk.Entry(f); ts.pack()
    tk.Label(f, text="Nom:").pack(pady=5)
    nom = tk.Entry(f); nom.pack()
    tk.Label(f, text="Cognom:").pack(pady=5)
    cog = tk.Entry(f); cog.pack()
    tk.Label(f, text="Data (AAAA-MM-DD):").pack(pady=5)
    data = tk.Entry(f); data.pack()
    
    # Botó per guardar les dades cridant a la funció d'inserció
    ttk.Button(f, text="Registrar Pacient", 
           command=lambda: insertar_pacient_db(ts.get(), nom.get(), cog.get(), "", data.get()) and f.destroy()).pack(pady=20)

def on_tab_changed(event):
    """Restringeix l'accés a certes pestanyes només per a l'administrador."""
    tab = event.widget.tab(event.widget.select(), "text")
    # Si la pestanya és de gestió, demana credencials d'admin
    if tab in ["Registrar Personal", "Manteniment"]:
        if not verify_admin_credentials():
            messagebox.showwarning("Accés Denegat", "Aquesta àrea és només per a l'administrador.")
            event.widget.select(0) # Torna automàticament a la pestanya de Login

# ============================================================
# CONFIGURACIÓ DE LA INTERFÍCIE GRÀFICA PRINCIPAL
# ============================================================

root = tk.Tk()
root.title("UA Hospital - Gestió de Personal")
root.geometry("450x650")
root.resizable(False, False)
root.configure(bg="#f0f4f7")

# Configuració d'estils per a un aspecte més modern
style = ttk.Style()
style.theme_use('clam')
style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'), padding=[10, 5])
style.configure('TButton', font=('Arial', 10, 'bold'))

# Títol de l'aplicació
tk.Label(root, text="🏥 UA - Gestió Hospitalària", font=("Arial", 16, "bold"), 
          bg="#f0f4f7", fg="#2c3e50").pack(pady=15)

# Creació del contenidor de pestanyes
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=20, pady=5)
# Enllaç de l'esdeveniment de canvi de pestanya amb la funció de seguretat
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
# Generació dinàmica de camps de text per al registre
fields = [("DNI*", "reg_dni"), ("Nom*", "reg_nom"), ("Primer Cognom*", "reg_c1"), ("Segon Cognom", "reg_c2"), ("Email*", "reg_email")]
for lbl, var_name in fields:
    tk.Label(f_reg, text=lbl, bg="white", font=("Arial", 8)).pack(pady=(4,0))
    en = tk.Entry(f_reg, width=35)
    en.pack()
    globals()[var_name] = en # Desa la referència de l'Entry de forma global

# Selector de Rol (Desplegable)
reg_role = ttk.Combobox(f_reg, values=["metge", "infermer", "vari"], state="readonly", width=32); reg_role.set("metge"); reg_role.pack(pady=5)
tk.Frame(f_reg, height=1, bg="#dee2e6").pack(fill="x", padx=40, pady=10) # Línia divisòria

tk.Label(f_reg, text="👤 Username*", bg="white", font=("Arial", 8)).pack()
reg_user = tk.Entry(f_reg, width=35); reg_user.pack()
tk.Label(f_reg, text="🔒 Password*", bg="white", font=("Arial", 8)).pack()
reg_pass = tk.Entry(f_reg, show="*", width=35); reg_pass.pack()
ttk.Button(f_reg, text="Registrar a la DB", command=register_user).pack(pady=20)

# --- PESTANYA MANTENIMENT ---
f_maint = tk.Frame(notebook, bg="white")
notebook.add(f_maint, text="Manteniment")
tk.Label(f_maint, text="🛠️ Gestió de l'Hospital", font=("Arial", 11, "bold"), bg="white").pack(pady=20)
ttk.Button(f_maint, text="3.2 Alta de Pacients", width=30, command=obrir_alta_pacient).pack(pady=10)
# Accés ràpid a altres funcionalitats (informatives en aquest cas)
ttk.Button(f_maint, text="3.4/3.5 Veure Operacions/Visites", width=30, 
            command=lambda: messagebox.showinfo("Info", "Funcions de consulta configurades a auth_ok.py")).pack(pady=10)

# Peu de pàgina informatiu
tk.Label(root, text="Base de Dades: PostgreSQL | Projecte ASIX 2026", bg="#f0f4f7", fg="gray", font=("Arial", 7)).pack(pady=5)

# Inici del bucle principal de l'aplicació
root.mainloop()