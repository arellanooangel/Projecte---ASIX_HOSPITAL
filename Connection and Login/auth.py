# ------------------------------
# -- Importació de llibreries --
# ------------------------------

import hashlib
from tkinter import messagebox, simpledialog
from db_connexio import get_connection

# ---------------------------
# -- Funció de xifrat SHA-256
# ---------------------------

def hash_password(password):
    """
    Converteix la contrasenya en un hash SHA-256
    per evitar guardar-la en text pla.
    """
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------------------------------------------
# -- Verificació de credencials d'administrador --
# ---------------------------------------------------

def verify_admin_credentials():
    """
    Demana les credencials de l'administrador quan s'accedeix
    a la pestanya 'Registrar Personal'. Només permet l'accés
    si l'usuari és 'ua-admin' i té rol 'admin'.
    """
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

    connection = get_connection()

    if not connection:
        messagebox.showerror("Error", "No es pot connectar a la base de dades.")
        return False

    try:
        cursor = connection.cursor()

        query = """
            SELECT role FROM usuaris
            WHERE username = %s AND password = %s
        """
        cursor.execute(query, (username, hash_password(password)))
        result = cursor.fetchone()

        if result and result[0] == "admin" and username == "ua-admin":
            messagebox.showinfo(
                "Accés concedit",
                "Benvingut administrador."
            )
            return True
        else:
            messagebox.showerror(
                "Accés denegat",
                "Credencials incorrectes o sense permisos d'administrador."
            )
            return False

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Error en la verificació: {e}"
        )
        return False

    finally:
        cursor.close()
        connection.close()

# ------------------------------
# -- Registre d'usuaris --
# ------------------------------

def register_user_db(username, password, role):
    """
    Registra un nou usuari a la base de dades PostgreSQL.
    """
    connection = get_connection()

    if not connection:
        messagebox.showerror("Error", "No es pot connectar a la base de dades.")
        return False

    try:
        cursor = connection.cursor()

        # Comprovar si l'usuari ja existeix
        cursor.execute(
            "SELECT username FROM usuaris WHERE username = %s",
            (username,)
        )
        if cursor.fetchone():
            messagebox.showerror("Error", "L'usuari ja existeix.")
            return False

        # Inserir usuari
        query = """
            INSERT INTO usuaris (username, password, role)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (
            username,
            hash_password(password),
            role
        ))

        connection.commit()
        messagebox.showinfo("Èxit", "Usuari registrat correctament.")
        return True

    except Exception as e:
        messagebox.showerror("Error", f"Error en el registre: {e}")
        return False

    finally:
        cursor.close()
        connection.close()

# ------------------------------
# -- Inici de sessió --
# ------------------------------

def login_user_db(username, password):
    """
    Verifica les credencials d'un usuari contra PostgreSQL.
    Retorna el rol si el login és correcte.
    """
    connection = get_connection()

    if not connection:
        messagebox.showerror("Error", "No es pot connectar a la base de dades.")
        return None

    try:
        cursor = connection.cursor()

        query = """
            SELECT role FROM usuaris
            WHERE username = %s AND password = %s
        """
        cursor.execute(query, (username, hash_password(password)))
        result = cursor.fetchone()

        if result:
            role = result[0]
            messagebox.showinfo(
                "Benvingut",
                f"Benvingut/da {username}!\nRol: {role}"
            )
            return role
        else:
            messagebox.showerror(
                "Error",
                "Usuari o contrasenya incorrectes."
            )
            return None

    except Exception as e:
        messagebox.showerror("Error", f"Error en el login: {e}")
        return None

    finally:
        cursor.close()
        connection.close()