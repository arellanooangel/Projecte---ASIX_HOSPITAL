import psycopg2
from faker import Faker
import random
# Importem la teva pròpia connexió
from db_connexio_ok import get_connection

# Inicialitzem Faker amb idiomes: Català i Rus (pel ciríl·lic)
fake = Faker(['ca_ES', 'ru_RU'])

def generar_dades_mestres():
    """Genera Especialitats, Plantes, Medicaments i Aparells bàsics."""
    conn = get_connection()
    if not conn:
        print("No hi ha connexió.")
        return

    try:
        cur = conn.cursor()
        cur.execute("SET search_path TO hospital;")

        print("Generant dades mestres...")

        # 1. Especialitats
        especialitats = ['Traumatologia', 'Pediatria', 'Cardiologia', 'Neurologia', 'Dermatologia', 'Cirurgia General']
        for esp in especialitats:
            cur.execute("INSERT INTO especialitat (descripcio) VALUES (%s) ON CONFLICT DO NOTHING;", (esp,))
        
        # 2. Plantes
        plantes = ['Planta Baixa (Urgències)', 'Planta 1 (Cirurgia)', 'Planta 2 (Cardiologia)', 'Planta 3 (Materno-infantil)']
        for planta in plantes:
            cur.execute("INSERT INTO planta (descripcio) VALUES (%s) ON CONFLICT DO NOTHING;", (planta,))

        # 3. Medicaments (Noms inventats o barrejats)
        for _ in range(50):
            cur.execute("INSERT INTO medicament (nom) VALUES (%s);", (fake.word().capitalize() + "mol",))

        conn.commit()
        print("Dades mestres generades correctament.")

    except Exception as e:
        conn.rollback()
        print(f"Error generant dades: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    generar_dades_mestres()