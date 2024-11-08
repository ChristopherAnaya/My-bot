import discord
from Menu_Extras import create_card
import datetime
import time
from Databases.databases import load_data
cursor, cursor2, _, _, _, _ = load_data()

def paginate(allballs, page=1):
    start_index = (page - 1) * 25
    end_index = page * 25
    return allballs[start_index:end_index]

class Dropdown(discord.ui.Select):
    def __init__(self, allballs, page=1):
        options = [discord.SelectOption(label=f"#{x[2]} {x[1]}",
        description = f"ATK: {int(int(cursor2.execute('SELECT * FROM ball_data WHERE ball_name = ?', (x[1],)).fetchone()[2]) * (int(x[3].split(':')[0]) / 100 + 1 ))}" \
        f"({'+' if x[3].split(':')[0][0] != '-' else ''}{str(int(x[3].split(':')[0]))}%)∙" \
        f"HP: {int(int(cursor2.execute('SELECT * FROM ball_data WHERE ball_name = ?', (x[1],)).fetchone()[3]) * (int(x[3].split(':')[1]) / 100 + 1 ))}" \
        f"({'+' if x[3].split(':')[1][0] != '-' else ''}{str(int(x[3].split(':')[1]))}%)∙" \
        f"{''.join('/' if z == '-' else ' | ' if z == ' ' else z for z in x[4])}",
        emoji=cursor2.execute('SELECT * FROM ball_data WHERE ball_name = ?', (x[1],)).fetchone()[1]) for x in paginate(allballs, page)]
        super().__init__(placeholder="Make a selection", options=options)
        
    async def callback(self, interaction: discord.Interaction):
        choice = cursor.execute('SELECT * FROM catches WHERE catch_id = ? AND catch_name = ?', (self.values[0].split(" ")[0][1:], self.values[0].split(" ")[1])).fetchone()
        time_convert = "".join(x if x not in ["-", ":"] else " " for x in choice[-1]).split()
        dt = datetime.datetime(int(time_convert[0]), int(time_convert[1]), int(time_convert[2]), int(time_convert[3]), int(time_convert[4]))
        timestamp = int(time.mktime(dt.timetuple()))
        content = "\n".join([
            f"ID:`#{choice[2]}`",
            f"Caught on <t:{timestamp}:f> (<t:{timestamp}:R>)",
            "THIS IS PLACEHOLDER TEXT FOR WHEN I DECIDE I FEEL LIKE MAKING TRADING WORK",
            "",
            f"ATK: {int(int(cursor2.execute('SELECT * FROM ball_data WHERE ball_name = ?', (choice[1],)).fetchone()[2]) *  (int(choice[3].split(':')[0]) / 100 + 1 ))}" + \
            f" ({("+" if choice[3].split(':')[0][0] != "-" else "") + str(int(choice[3].split(':')[0]))}%)",
            f"HP: {int(int(cursor2.execute('SELECT * FROM ball_data WHERE ball_name = ?', (choice[1],)).fetchone()[3]) *  (int(choice[3].split(':')[1]) / 100 + 1 ))}" + \
            f" ({("+" if choice[3].split(':')[1][0] != "-" else "") + str(int(choice[3].split(':')[1]))}%)",
        ])

        with open(rf"C:\Users\Chris\OneDrive\Documents\Discord-Bot\Art\Card_art\{choice[1]}_Card.png", "rb") as image_file:  
            await interaction.response.send_message(content=content, file=discord.File(fp=create_card(int(int(cursor2.execute('SELECT * FROM ball_data WHERE ball_name = ?', (choice[1],)).fetchone()[2]) *  (int(choice[3].split(':')[0]) / 100 + 1 )),
            int(int(cursor2.execute('SELECT * FROM ball_data WHERE ball_name = ?', (choice[1],)).fetchone()[3]) *  (int(choice[3].split(':')[1]) / 100 + 1 )), choice[1],
            cursor2.execute('SELECT * FROM ball_data WHERE ball_name = ?', (choice[1],)).fetchone()[4],
            cursor2.execute('SELECT * FROM ball_data WHERE ball_name = ?', (choice[1],)).fetchone()[5]), filename="card.png"))
