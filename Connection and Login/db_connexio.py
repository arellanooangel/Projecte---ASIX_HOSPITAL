import psycopg2

def get_connection():
    try:
        connection = psycopg2.connect(
            host="192.168.2.5",
            database="hospital",
            user="postgres",
            password="1234",
            port=5432
        )
        return connection

    except Exception as e:
        print("Error de connexió:", e)
        return None