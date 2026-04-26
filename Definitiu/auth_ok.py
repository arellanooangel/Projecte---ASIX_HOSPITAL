import psycopg2
from tkinter import messagebox, simpledialog
from db_connexio_ok import get_connection

def login_user_db(username, password):
    """Verifica les credencials (Apartat 3.1)."""
    conn = get_connection()
    if not conn: return None
    try:
        cur = conn.cursor()
        cur.execute("SET search_path TO hospital;")
        query = """
            SELECT u.id_personal, p.nom, p.cognom1 
            FROM usuaris u
            JOIN personal p ON u.id_personal = p.id_personal
            WHERE u.username = %s 
              AND u.password = encode(digest(%s, 'sha256'), 'hex')
              AND u.estat = 'actiu'
        """
        cur.execute(query, (username, password))
        result = cur.fetchone()
        if not result: return None
        
        id_p, nom, cognom = result
        if username == 'ua-admin': return ("admin", nom, cognom)
        
        for role in ['metge', 'infermer', 'vari']:
            cur.execute(f"SELECT 1 FROM {role} WHERE id_personal = %s", (id_p,))
            if cur.fetchone(): return (role, nom, cognom)
        return ("usuari", nom, cognom)
    finally:
        conn.close()

def register_personal_db(dni, nom, c1, c2, email, username, password, role):
    """Insereix nou personal i usuari (Apartat 3.1 i 3.3)."""
    conn = get_connection()
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute("SET search_path TO hospital;")
        cur.execute("INSERT INTO personal (dni, nom, cognom1, cognom2, email) VALUES (%s,%s,%s,%s,%s) RETURNING id_personal", 
                    (dni, nom, c1, c2, email))
        id_p = cur.fetchone()[0]
        cur.execute("INSERT INTO usuaris (username, password, estat, id_personal) VALUES (%s, encode(digest(%s, 'sha256'), 'hex'), 'actiu', %s)", 
                    (username, password, id_p))
        cur.execute(f"INSERT INTO {role} (id_personal) VALUES (%s)", (id_p,))
        conn.commit()
        return True
    except Exception as e:
        if conn: conn.rollback()
        return False
    finally:
        conn.close()

def insertar_pacient_db(ts, nom, c1, data):
    """Alta de pacients (Apartat 3.2)."""
    conn = get_connection()
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO hospital.pacient (targeta_sanitaria, nom, cognom1, data_naixement) VALUES (%s, %s, %s, %s)", 
                    (ts, nom, c1, data))
        conn.commit()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"No s'ha pogut registrar el pacient: {e}")
        return False
    finally:
        conn.close()

def verify_admin_credentials():
    """Validació per a pestanyes restringides."""
    u = simpledialog.askstring("Admin", "Usuari administrador:")
    if not u: return False
    p = simpledialog.askstring("Admin", "Contrasenya:", show="*")
    res = login_user_db(u, p)
    return res is not None and res[0] == "admin"