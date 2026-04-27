from tkinter import messagebox, simpledialog
from db_connexio_ok import get_connection

def login_user_db(username, password):
    """Verifica las credenciales en la tabla usuaris con hash SHA-256."""
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
    except Exception as e:
        messagebox.showerror("Error Login", f"Error: {e}")
        return None
    finally:
        if conn: conn.close()

def register_personal_db(dni, nom, c1, c2, email, username, password, role):
    """Inserta un nuevo trabajador. El DNI se pasa a mayúsculas para el Trigger."""
    conn = get_connection()
    if not conn: return False
    dni = dni.upper() 
    try:
        cur = conn.cursor()
        cur.execute("SET search_path TO hospital;")
        
        cur.execute("""
            INSERT INTO personal (dni, nom, cognom1, cognom2, email)
            VALUES (%s, %s, %s, %s, %s) RETURNING id_personal
        """, (dni, nom, c1, c2, email if email else None))
        id_pers = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO usuaris (username, password, estat, id_personal)
            VALUES (%s, encode(digest(%s, 'sha256'), 'hex'), 'actiu', %s)
        """, (username, password, id_pers))

        if role == "metge":
            cur.execute("SELECT id_especialitat FROM hospital.especialitat LIMIT 1")
            res_esp = cur.fetchone()
            id_esp = res_esp[0] if res_esp else 1
            cur.execute("INSERT INTO hospital.metge VALUES (%s, %s, %s, %s)", 
                       (id_pers, "Grau Medicina", "Sense exp.", id_esp))
        elif role == "infermer":
            cur.execute("INSERT INTO hospital.infermer VALUES (%s, %s, %s)", 
                       (id_pers, "Grau Infermeria", "Sense exp."))
        elif role == "vari":
            cur.execute("INSERT INTO hospital.vari VALUES (%s, %s)", 
                       (id_pers, "Administració"))

        conn.commit()
        return True
    except Exception as e:
        if conn: conn.rollback()
        messagebox.showerror("Error Registre", f"Error de validación o BD:\n{e}")
        return False
    finally:
        if conn: conn.close()

def insertar_pacient_db(ts, nom, c1, c2, data_naix):
    """Inserta un paciente con los 5 campos requeridos por la tabla 'pacient'."""
    conn = get_connection()
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute("SET search_path TO hospital;")
        cur.execute("""
            INSERT INTO pacient (targeta_sanitaria, nom, cognom1, cognom2, data_naixement)
            VALUES (%s, %s, %s, %s, %s)
        """, (ts, nom, c1, c2 if c2 else None, data_naix))
        conn.commit()
        return True
    except Exception as e:
        if conn: conn.rollback()
        messagebox.showerror("Error Pacient", f"Error al insertar: {e}")
        return False
    finally:
        if conn: conn.close()

def verify_admin_credentials():
    u = simpledialog.askstring("Validación", "Usuari administrador:")
    p = simpledialog.askstring("Validación", "Contrasenya:", show="*")
    if not u or not p: return False
    res = login_user_db(u, p)
    return res is not None and res[0] == "admin"