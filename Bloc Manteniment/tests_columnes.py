from auth_ok import get_connection

def llistar_columnes():
    conn = get_connection()
    cur = conn.cursor()
    # Canvia 'pacient' per 'hospital.pacient' si cal
    cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'pacient'
    """)
    columnes = cur.fetchall()
    print("Les teves columnes reals són:")
    for col in columnes:
        print(f"- {col[0]}")
    conn.close()

llistar_columnes()