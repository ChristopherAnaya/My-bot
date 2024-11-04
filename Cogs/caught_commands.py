from discord.ext import commands
from databases.databases import load_data
cursor, cursor2, conn, conn2 = load_data()

class CaughtCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def caught(self, ctx):
        cursor, _, _, _ = load_data()  # Ensure to load the database connection here
        cursor.execute('SELECT * FROM catches WHERE user_id = ?', (ctx.author.id,))
        user_catches = cursor.fetchall()
        
        if user_catches:
            catches_list = "\n".join([f"{catch[1]}, {catch[2]}, {catch[3]}, {catch[4]}" for catch in user_catches])
            await ctx.reply(f"Your catches:\n{catches_list}")
        else:
            await ctx.reply("No catches found for you.")

async def setup(bot):
    await bot.add_cog(CaughtCommands(bot))