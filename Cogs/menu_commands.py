import discord
from discord.ext import commands
from discord import app_commands
from Menu_Extras import DropdownView
from Databases.databases import load_data
cursor, _, _, _, _, _ = load_data()

class MenuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="menu", description="Shows your completion of owned and missing TestBalls.")
    async def show_menu(self, interaction: discord.Interaction):
        result = cursor.execute('SELECT * FROM catches WHERE user_id = ?', (interaction.user.id,)).fetchone()
        if not result:
            await interaction.response.send_message("You don't have any testballs yet!")
        else:    
            allballs = cursor.execute('SELECT * FROM catches WHERE user_id = ?', (interaction.user.id,)).fetchall()
            await interaction.response.send_message("Choose an option:", view=DropdownView(allballs, 1, interaction.user.id))

async def setup(bot):
    if bot.tree.get_command("menu"):
        bot.tree.remove_command("menu")
    await bot.add_cog(MenuCog(bot))