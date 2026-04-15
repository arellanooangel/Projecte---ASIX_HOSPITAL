# ------------------------------
# -- Connexió a PostgreSQL --
# ------------------------------

import psycopg2
from psycopg2 import OperationalError

def get_connection():
    """
    Estableix una connexió amb la base de dades PostgreSQL.
    Modifica aquests paràmetres segons la teva configuració.
    """
    try:
        connection = psycopg2.connect(
            host="192.168.2.5",       # Servidor de la base de dades
            database="hospital",    # Nom de la base de dades
            user="postgres",        # Usuari de PostgreSQL
            password="1234",    # Contrasenya de PostgreSQL
            port="5432"             # Port per defecte
        )
        return connection
    except OperationalError as e:
        print(f"Error de connexió a PostgreSQL: {e}")
        return None