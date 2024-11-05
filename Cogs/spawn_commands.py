import discord
from discord.ext import commands
from discord.ui import Modal, TextInput, Button, View
import random
import os
import datetime
from Databases.databases import load_data

cursor, _, cursor3, conn, _, conn3 = load_data()

files = os.listdir(r"C:\Users\Chris\OneDrive\Documents\Discord-Bot\Art\Spawn Arts")

class UserInfoModal(Modal):
    def __init__(self, view, button, clicked, current):
        super().__init__(title="Catch This Testball!")
        self.button = button
        self.view = view
        self.clicked = clicked
        self.current = current
        self.name_input = TextInput(label="Name Of This Ball", placeholder="Your Guess")
        self.add_item(self.name_input)
    async def on_submit(self, interaction: discord.Interaction):
        name = (self.name_input.value).strip().title()
        if self.clicked == True:
            await interaction.response.send_message(f"{interaction.user.mention} I was caught already!")
        elif name + ".png" == self.current:
            self.button.disabled = True 
            ballname = name
            ballstats = f"{str(random.randint(-20, 20))}:{str(random.randint(-20, 20))}"
            balltime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            ballstatsuse = "/".join([("+" if x[0] != "-" else "") + x + "%" for x in ballstats.split(":")])
            cursor.execute('SELECT COUNT(*) FROM catches WHERE catch_name = ?', (name,))
            ballid = str(cursor.fetchone()[0] + 1).zfill(8)
            if not cursor3.execute('SELECT * FROM user_data WHERE user_id = ? AND ball_name = ?', (str(interaction.user.id), ballname,)).fetchall():
                cursor3.execute('INSERT INTO user_data (user_id, ball_name) VALUES (?, ?)', (str(interaction.user.id), ballname)) 
                conn3.commit()
            cursor.execute('INSERT INTO catches (user_id, catch_name, catch_id, catch_stats, catch_time) VALUES (?, ?, ?, ?, ?)', (str(interaction.user.id), ballname, ballid, ballstats, balltime))
            conn.commit()
            await interaction.response.send_message(f"{interaction.user.mention} You caught **{name}!** `(#{ballid}, {ballstatsuse})`")
            await interaction.message.edit(view=self.view)
            self.clicked = True
        else:
            await interaction.response.send_message(f"{interaction.user.mention} Wrong Name!")

class ImageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clicked = False  
        self.current = None
    
    @commands.command()
    async def image(self, ctx):
        self.current = random.choice(files)
        button = Button(label="Click Me!", style=discord.ButtonStyle.primary)
     
        async def button_callback(interaction):
            modal = UserInfoModal(view, button, self.clicked, self.current)
            await interaction.response.send_modal(modal)

        button.callback = button_callback
        view = View()
        view.add_item(button)
        await ctx.send(content="A wild testingball appeared!", file=discord.File(fr"C:\Users\Chris\OneDrive\Documents\Discord-Bot\Art\Spawn Arts\{self.current}"), view=view)

async def setup(bot):
    await bot.add_cog(ImageCog(bot))