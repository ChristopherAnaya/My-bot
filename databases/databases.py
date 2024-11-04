import sqlite3



def load_data():
    conn = sqlite3.connect("catch_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS catches (    
            user_id TEXT,
            catch_name TEXT,
            catch_id TEXT,
            catch_stats TEXT,
            catch_time TEXT
        )
    ''')
    conn.commit()
    conn2 = sqlite3.connect('ball_data.db')
    cursor2 = conn2.cursor()
    cursor2.execute('''
        CREATE TABLE IF NOT EXISTS ball_data (
            ball_name TEXT PRIMARY KEY,
            emoji_id TEXT,
            base_atk TEXT,
            base_hp TEXT          
        )
    ''')
    conn.commit()
    return cursor, cursor2, conn, conn2