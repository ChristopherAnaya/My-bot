import discord
from discord.ext import commands
from discord.ui import View
from Menu_Extras.card_maker import create_card
import datetime
import time
from Databases.databases import load_data
cursor, cursor2, _, _, _, _ = load_data()

def paginate(allballs, page=1):
    start_index = (page - 1) * 25
    end_index = page * 25
    return allballs[start_index:end_index]

class MenuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def show_menu(self, ctx):
        result = cursor.execute('SELECT * FROM catches WHERE user_id = ?', (ctx.author.id,)).fetchone()
        if not result:
            await ctx.reply("You don't have any testballs yet!")
        else:
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

            class QuitButton(discord.ui.Button):
                def __init__(self):
                    super().__init__(label="Quit", style=discord.ButtonStyle.danger)

                async def callback(self, interaction: discord.Interaction):
                    await interaction.response.defer()
                    for child in self.view.children:
                        child.disabled = True
                    await interaction.edit_original_response(view=self.view)

            class PageButton(discord.ui.Button):
                def __init__(self, label, page, allballs, disabled=False, style=discord.ButtonStyle.secondary):
                    super().__init__(label=label, style=style, disabled=disabled)
                    self.page = page
                    self.allballs = allballs
                async def callback(self, interaction: discord.Interaction):
                    await interaction.response.defer()
                    current_page = self.view.page
                    new_page = current_page + 1 if self.page == "next" else current_page - 1 if self.page == "previous" else 1 if self.page == "<<" else (len(allballs) + 24)//25
                    if new_page == 1:
                        self.view.children[1].disabled = True
                        self.view.children[3].disabled = False
                    elif new_page == (len(allballs) + 24)//25:
                        self.view.children[3].disabled = True
                        self.view.children[1].disabled = False
                    else:
                        self.view.children[3].disabled = False
                        self.view.children[1].disabled = False  
                    self.view.children[2].label = new_page
                    self.view.children[1].label = new_page - 1 if new_page - 1 > 0 else "..."
                    self.view.children[3].label = new_page + 1 if new_page + 1 <= (len(allballs) + 24)//25 else "..."

                    self.view.page = new_page#maybe delete this we will see
                    
                    paginated_balls = paginate(allballs, new_page)
                    self.view.children[6].options = [
                        discord.SelectOption(
                            label=f"#{x[2]} {x[1]}",
                            description=f"ATK: {int(int(cursor2.execute('SELECT * FROM ball_data WHERE ball_name = ?', (x[1],)).fetchone()[2]) * (int(x[3].split(':')[0]) / 100 + 1 ))} " \
                                        f"({'+' if x[3].split(':')[0][0] != '-' else ''}{str(int(x[3].split(':')[0]))}%)∙" \
                                        f"HP: {int(int(cursor2.execute('SELECT * FROM ball_data WHERE ball_name = ?', (x[1],)).fetchone()[3]) * (int(x[3].split(':')[1]) / 100 + 1 ))} " \
                                        f"({'+' if x[3].split(':')[1][0] != '-' else ''}{str(int(x[3].split(':')[1]))}%)",
                            emoji=cursor2.execute('SELECT * FROM ball_data WHERE ball_name = ?', (x[1],)).fetchone()[1]
                        )
                        for x in paginated_balls
                    ]
                    await interaction.edit_original_response(view=self.view)

            class CurrentButton(discord.ui.Button):
                def __init__(self, label, disabled=True):
                    super().__init__(label=label, style=discord.ButtonStyle.secondary, disabled=disabled)
            
            class DropdownView(View):
                def __init__(self, allballs, page):
                    super().__init__()
                    self.allballs = allballs  
                    self.page = page
                    if len(allballs) <= 25:
                        self.add_item(Dropdown(allballs, page))
                        self.add_item(QuitButton())
                    else:
                        self.add_item(PageButton(label="<<", page="<<", allballs=allballs))
                        self.add_item(PageButton(label="...", page="previous", allballs=allballs, disabled=True, style=discord.ButtonStyle.primary))
                        self.add_item(CurrentButton(label="1"))
                        self.add_item(PageButton(label="2", page="next", allballs=allballs, style=discord.ButtonStyle.primary))
                        self.add_item(PageButton(label=">>", page=">>", allballs=allballs))
                        self.add_item(QuitButton())
                        self.add_item(Dropdown(allballs, page))
            
            allballs = cursor.execute('SELECT * FROM catches WHERE user_id = ?', (ctx.author.id,)).fetchall()
            await ctx.reply("Choose an option:", view=DropdownView(allballs,1))

async def setup(bot):
    await bot.add_cog(MenuCog(bot)) 