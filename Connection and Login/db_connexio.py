import psycopg2

def get_connection():
    try:
        connection = psycopg2.connect(
            host="192.168.2.5",
            database="hospital",
            user="postgres",
            password="1234",
            sslmode="require"  # Força el xifrat SSL amb el certificat autofirmat
        )
        return connection
    except Exception as e:
        print(f"Error: {e}")
        return None