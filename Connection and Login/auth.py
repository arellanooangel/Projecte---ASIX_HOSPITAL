from tkinter import messagebox, simpledialog
from db_connexio import get_connection


# ------------------------------
# ADMIN VERIFICACIÓ
# ------------------------------

def verify_admin_credentials():
    username = simpledialog.askstring(
        "Autenticació d'administrador",
        "Introdueix el nom d'usuari administrador:"
    )

    if username is None:
        return False

    password = simpledialog.askstring(
        "Autenticació d'administrador",
        "Introdueix la contrasenya:",
        show="*"
    )

    if password is None:
        return False

    conn = get_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT role
            FROM usuaris
            WHERE username = %s
            AND password = encode(digest(%s,'sha256'),'hex')
        """, (username, password))

        result = cur.fetchone()

        return bool(result and result[0] == "admin")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return False

    finally:
        cur.close()
        conn.close()


# ------------------------------
# REGISTRE
# ------------------------------

def register_user_db(username, password, role):
    conn = get_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()

        cur.execute("SELECT username FROM usuaris WHERE username=%s", (username,))
        if cur.fetchone():
            messagebox.showerror("Error", "Usuari ja existeix")
            return False

        cur.execute("""
            INSERT INTO usuaris (username, password, role)
            VALUES (%s, encode(digest(%s,'sha256'),'hex'), %s)
        """, (username, password, role))

        conn.commit()
        messagebox.showinfo("OK", "Usuari registrat")
        return True

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return False

    finally:
        cur.close()
        conn.close()


# ------------------------------
# LOGIN
# ------------------------------

def login_user_db(username, password):
    conn = get_connection()

    if not conn:
        return None

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT role
            FROM usuaris
            WHERE username=%s
            AND password=encode(digest(%s,'sha256'),'hex')
        """, (username, password))

        result = cur.fetchone()

        return result[0] if result else None

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

    finally:
        cur.close()
        conn.close()