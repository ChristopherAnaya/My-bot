from discord.ext import commands
from Menu_Extras import DropdownView
from Databases.databases import load_data
cursor, _, _, _, _, _ = load_data()

class MenuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def show_menu(self, ctx):
        result = cursor.execute('SELECT * FROM catches WHERE user_id = ?', (ctx.author.id,)).fetchone()
        if not result:
            await ctx.reply("You don't have any testballs yet!")
        else:    
            allballs = cursor.execute('SELECT * FROM catches WHERE user_id = ?', (ctx.author.id,)).fetchall()
            await ctx.reply("Choose an option:", view=DropdownView(allballs,1))

async def setup(bot):
    await bot.add_cog(MenuCog(bot)) 