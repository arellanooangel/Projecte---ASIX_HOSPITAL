import psycopg2
from tkinter import messagebox, simpledialog
from db_connexio import get_connection

def login_user_db(username, password):
    """Verifica les credencials a la taula usuaris amb hash SHA-256."""
    conn = get_connection()
    if not conn: return None
    try:
        cur = conn.cursor()
        # Aseguramos que estamos en el esquema correcto
        cur.execute("SET search_path TO hospital;")
        
        # Consulta para obtener el ID y los datos básicos del personal en un solo JOIN
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
        
        # Si es el admin por defecto definido en tu SQL
        if username == 'ua-admin':
            return ("admin", result[1], result[2])
        
        id_p = result[0]
        # Cerquem el rol real en las tablas hijas
        for role in ['metge', 'infermer', 'vari']:
            cur.execute(f"SELECT 1 FROM {role} WHERE id_personal = %s", (id_p,))
            if cur.fetchone():
                return (role, result[1], result[2])
            
        return ("usuari", result[1], result[2])
        
    except Exception as e:
        messagebox.showerror("Error Login", f"Error de connexió: {e}")
        return None
    finally:
        conn.close()

def register_personal_db(dni, nom, c1, c2, email, username, password, role):
    """Insereix en 3 taules: personal, usuaris i la taula del rol triat."""
    conn = get_connection()
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute("SET search_path TO hospital;")
        
        # 1. Inserir a 'personal'
        cur.execute("""
            INSERT INTO personal (dni, nom, cognom1, cognom2, email)
            VALUES (%s, %s, %s, %s, %s) RETURNING id_personal
        """, (dni, nom, c1, c2, email if email else None))
        id_pers = cur.fetchone()[0]

        # 2. Inserir a 'usuaris'
        cur.execute("""
            INSERT INTO usuaris (username, password, estat, id_personal)
            VALUES (%s, encode(digest(%s, 'sha256'), 'hex'), 'actiu', %s)
        """, (username, password, id_pers))

        # 3. Inserir a la taula de Rol específica (Seguint el teu SQL strict)
        if role == "metge":
            # Tu SQL pide: estudis, experiencia, id_especialitat (NOT NULL)
            cur.execute("""
                INSERT INTO metge (id_personal, estudis, experiencia, id_especialitat) 
                VALUES (%s, %s, %s, %s)
            """, (id_pers, "Grau en Medicina", "Sense experiència", 1)) 
            
        elif role == "infermer":
            # Tu SQL pide: curs, experiencia
            cur.execute("""
                INSERT INTO infermer (id_personal, curs, experiencia) 
                VALUES (%s, %s, %s)
            """, (id_pers, "Grau en Infermeria", "Sense experiència"))
            
        elif role == "vari":
            # Tu SQL pide: feina
            cur.execute("""
                INSERT INTO vari (id_personal, feina) 
                VALUES (%s, %s)
            """, (id_pers, "Administració"))

        conn.commit()
        return True
    except Exception as e:
        if conn: conn.rollback()
        messagebox.showerror("Error en Registre", f"Error de base de dades: {e}")
        return False
    finally:
        if conn: conn.close()

def verify_admin_credentials():
    """Popup per protegir pestanyes d'administració."""
    u = simpledialog.askstring("Validació", "Usuari administrador:")
    if not u: return False
    p = simpledialog.askstring("Validació", "Contrasenya:", show="*")
    if not p: return False
    
    res = login_user_db(u, p)
    # Comprovar si el primer element de la tupla retornada és 'admin'
    return res is not None and res[0] == "admin"