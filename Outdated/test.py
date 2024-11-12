import sqlite3

def add_favorites_column():
    conn = sqlite3.connect("catch_data.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE catches SET past_owner = NULL
    ''')
    
    conn.commit()
    conn.close()

add_favorites_column()