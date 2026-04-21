import psycopg2
from tkinter import messagebox, simpledialog
from db_connexio import get_connection

def login_user_db(username, password):
    """Verifica les credencials a la taula usuaris amb hash SHA-256."""
    conn = get_connection()
    if not conn: return None
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id_personal FROM usuaris 
            WHERE username = %s AND password = encode(digest(%s, 'sha256'), 'hex')
            AND estat = 'actiu'
        """, (username, password))
        
        result = cur.fetchone()
        if not result: return None
        
        if username == 'ua-admin': return "admin"
        
        id_p = result[0]
        # Cerquem en quina taula de rol està registrat
        for role in ['metge', 'infermer', 'vari']:
            cur.execute(f"SELECT 1 FROM {role} WHERE id_personal = %s", (id_p,))
            if cur.fetchone(): return role
            
        return "usuari"
    except Exception as e:
        messagebox.showerror("Error Login", str(e))
        return None
    finally:
        conn.close()

def register_personal_db(dni, nom, c1, c2, email, username, password, role):
    """
    Insereix en 3 taules: personal, usuaris i la taula del rol triat.
    """
    conn = get_connection()
    if not conn: return False
    try:
        cur = conn.cursor()
        
        # 1. Inserir a 'personal'
        cur.execute("""
            INSERT INTO personal (dni, nom, cognom1, cognom2, email)
            VALUES (%s, %s, %s, %s, %s) RETURNING id_personal
        """, (dni, nom, c1, c2, email))
        id_pers = cur.fetchone()[0]

        # 2. Inserir a 'usuaris'
        cur.execute("""
            INSERT INTO usuaris (username, password, estat, id_personal)
            VALUES (%s, encode(digest(%s, 'sha256'), 'hex'), 'actiu', %s)
        """, (username, password, id_pers))

        # 3. Inserir a la taula de Rol específica
        if role == "metge":
            # Per defecte id_especialitat 1 (ha d'existir a la teva taula especialitat)
            cur.execute("INSERT INTO metge (id_personal, estudis, id_especialitat) VALUES (%s, %s, %s)", 
                       (id_pers, "Grau en Medicina", 1))
        elif role == "infermer":
            cur.execute("INSERT INTO infermer (id_personal, curs) VALUES (%s, %s)", 
                       (id_pers, "Grau en Infermeria"))
        elif role == "vari":
            cur.execute("INSERT INTO vari (id_personal, feina) VALUES (%s, %s)", 
                       (id_pers, "Administratiu/Altres"))

        conn.commit()
        return True
    except Exception as e:
        if conn: conn.rollback()
        messagebox.showerror("Error en Registre", f"No s'ha pogut completar: {e}")
        return False
    finally:
        if conn: conn.close()

def verify_admin_credentials():
    """Popup per protegir pestanyes d'administració."""
    u = simpledialog.askstring("Admin", "Usuari administrador:")
    if not u: return False
    p = simpledialog.askstring("Admin", "Contrasenya:", show="*")
    if not p: return False
    return login_user_db(u, p) == "admin"