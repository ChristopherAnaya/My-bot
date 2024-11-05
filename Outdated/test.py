import sqlite3
conn3 = sqlite3.connect('user_data.db')
cursor3 = conn3.cursor()
cursor3.execute('INSERT INTO user_757769769242853436data (user_id, ball_name) VALUES (?, ?)', (input("id"), input("ball")))
conn3.commit()