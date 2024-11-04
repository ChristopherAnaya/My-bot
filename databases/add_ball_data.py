import sqlite3
conn = sqlite3.connect('ball_data.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS ball_data (
        ball_name TEXT PRIMARY KEY,
        emoji_id TEXT,
        base_atk TEXT,
        base_hp TEXT          
    )
''')
conn.commit()

def add_ball():
    ball_name = input("Enter the ball name: ")
    emoji_id = input("Enter the emoji ID: ")
    base_atk = input("Enter the ATK: ")
    base_hp = input("Enter the HP: ")
    try:
        c.execute('INSERT INTO ball_data (ball_name, emoji_id, base_atk, base_hp) VALUES (?, ?, ?, ?)', (ball_name, emoji_id, base_atk, base_hp))
        conn.commit()
        print(f"Ball '{ball_name}' with ID {emoji_id} with ATK {base_atk} with HP {base_hp} added successfully.")
    except sqlite3.IntegrityError:
        print(f"Error: '{ball_name}' already exists in the database.")
while True:
    add_ball()
    cont = input("Do you want to add another ball? (yes/no): ").strip().lower()
    if cont != 'yes':
        break
conn.close()