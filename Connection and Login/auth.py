import hashlib
from tkinter import messagebox
from db_connexio import get_connection


# ----------------------
# XIFRAR CONTRASENYA
# ----------------------

def hash_password(password):
    """
    Converteix la contrasenya a SHA-256
    per evitar guardar text pla a la base de dades
    """
    return hashlib.sha256(password.encode()).hexdigest()


# ----------------------
# REGISTRAR USUARI
# ----------------------

def register_user_db(username, password, role):
    """
    Registra un usuari nou a PostgreSQL
    amb validació d'existència prèvia
    """

    connection = get_connection()

    if not connection:
        messagebox.showerror("Error", "No s'ha pogut connectar a la base de dades.")
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

        # Inserir usuari nou
        cursor.execute("""
            INSERT INTO usuaris (username, password, role)
            VALUES (%s, %s, %s)
        """, (
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


# ----------------------
# INICIAR SESSIÓ
# ----------------------

def login_user_db(username, password):
    """
    Valida l'usuari contra PostgreSQL
    i retorna el rol si és correcte
    """

    connection = get_connection()

    if not connection:
        messagebox.showerror("Error", "No s'ha pogut connectar a la base de dades.")
        return False

    try:
        cursor = connection.cursor()

        # Buscar usuari amb contrasenya xifrada
        cursor.execute("""
            SELECT role 
            FROM usuaris 
            WHERE username = %s AND password = %s
        """, (
            username,
            hash_password(password)
        ))

        result = cursor.fetchone()

        if result:
            role = result[0]

            messagebox.showinfo(
                "Benvingut/da",
                f"Benvingut/da {username}!\nRol: {role}"
            )
            return True

        else:
            messagebox.showerror(
                "Error",
                "Usuari o contrasenya incorrectes."
            )
            return False

    except Exception as e:
        messagebox.showerror("Error", f"Error en el login: {e}")
        return False

    finally:
        cursor.close()
        connection.close()