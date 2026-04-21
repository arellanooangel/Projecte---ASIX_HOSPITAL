import psycopg2
from tkinter import messagebox, simpledialog
from db_connexio import get_connection

def login_user_db(username, password):
    """
    Verifica les credencials a la taula usuaris amb hash SHA-256.
    Retorna una tupla (rol, nom, cognom) o None si falla.
    """
    conn = get_connection()
    if not conn: return None
    try:
        cur = conn.cursor()
        # Seleccionem l'esquema correcte
        cur.execute("SET search_path TO hospital;")
        
        # Consulta per verificar usuari i obtenir dades personals (JOIN)
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
        
        if not result:
            return None
        
        id_p, nom, cognom = result
        
        # Cas especial: Admin per defecte
        if username == 'ua-admin':
            return ("admin", nom, cognom)
        
        # Determinar el rol real consultant les taules especialitzades
        for role in ['metge', 'infermer', 'vari']:
            cur.execute(f"SELECT 1 FROM {role} WHERE id_personal = %s", (id_p,))
            if cur.fetchone():
                return (role, nom, cognom)
            
        return ("usuari", nom, cognom)
        
    except Exception as e:
        messagebox.showerror("Error Login", f"Error en la consulta: {e}")
        return None
    finally:
        conn.close()

def register_personal_db(dni, nom, c1, c2, email, username, password, role):
    """
    Insereix un nou treballador en 3 passos: 
    1. Dades personals, 2. Usuari de sistema, 3. Taula de rol.
    """
    conn = get_connection()
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute("SET search_path TO hospital;")
        
        # --- PAS 1: Taula 'personal' ---
        cur.execute("""
            INSERT INTO personal (dni, nom, cognom1, cognom2, email)
            VALUES (%s, %s, %s, %s, %s) RETURNING id_personal
        """, (dni, nom, c1, c2, email if email else None))
        id_pers = cur.fetchone()[0]

        # --- PAS 2: Taula 'usuaris' ---
        cur.execute("""
            INSERT INTO usuaris (username, password, estat, id_personal)
            VALUES (%s, encode(digest(%s, 'sha256'), 'hex'), 'actiu', %s)
        """, (username, password, id_pers))

        # --- PAS 3: Taula de Rol (Metge, Infermer o Vari) ---
        if role == "metge":
            # COMPROVACIÓ D'ESPECIALITAT (Evita l'error de Foreign Key)
            cur.execute("SELECT id_especialitat FROM especialitat LIMIT 1")
            res_esp = cur.fetchone()
            
            if res_esp:
                id_esp = res_esp[0]
            else:
                # Si no n'hi ha cap, en creem una per defecte
                cur.execute("INSERT INTO especialitat (descripcio) VALUES (%s) RETURNING id_especialitat", ("Medicina General",))
                id_esp = cur.fetchone()[0]
                
            cur.execute("""
                INSERT INTO metge (id_personal, estudis, experiencia, id_especialitat) 
                VALUES (%s, %s, %s, %s)
            """, (id_pers, "Grau en Medicina", "Sense experiència previa", id_esp))
            
        elif role == "infermer":
            cur.execute("""
                INSERT INTO infermer (id_personal, curs, experiencia) 
                VALUES (%s, %s, %s)
            """, (id_pers, "Grau en Infermeria", "Sense experiència previa"))
            
        elif role == "vari":
            cur.execute("""
                INSERT INTO vari (id_personal, feina) 
                VALUES (%s, %s)
            """, (id_pers, "Administració / Serveis"))

        # Si tot ha anat bé, guardem els canvis
        conn.commit()
        return True

    except Exception as e:
        if conn: conn.rollback()
        messagebox.showerror("Error en Registre", f"Error de base de dades: {e}")
        return False
    finally:
        if conn: conn.close()

def verify_admin_credentials():
    """
    Sol·licita credencials d'administrador mitjançant quadres de diàleg 
    per permetre l'accés a pestanyes restringides.
    """
    u = simpledialog.askstring("Validació d'Accés", "Usuari administrador:")
    if not u: return False
    p = simpledialog.askstring("Validació d'Accés", "Contrasenya:", show="*")
    if not p: return False
    
    auth_res = login_user_db(u, p)
    # Comprovem si el primer element de la tupla és 'admin'
    return auth_res is not None and auth_res[0] == "admin"