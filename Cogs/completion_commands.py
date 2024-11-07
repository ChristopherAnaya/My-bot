#may need to add pages in the future but not now

import discord
from discord.ext import commands
from Databases.databases import load_data
_, cursor2, cursor3, _, _, _ = load_data()

class CompletionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def completion(self, ctx):

        emojis = {x[0]:x[1] for x in cursor2.execute('SELECT * FROM ball_data').fetchall()}
        owned = [x[1] for x in cursor3.execute('SELECT * FROM user_data WHERE user_id = ?', (str(ctx.author.id),)).fetchall()]
        not_owned = [x[0] for x in cursor2.execute('SELECT * FROM ball_data').fetchall()]
        
        for x in owned:
            del not_owned[not_owned.index(x)]
        owned = [emojis[x] for x in owned]
        not_owned = [emojis[x] for x in not_owned]
        
        embed = discord.Embed(description=f"Progression: **{len(owned) / len(emojis) * 100}%**", color=0x7289da)

        emojis_per_row = 10
        owned_rows = [owned[i:i + emojis_per_row] for i in range(0, len(owned), emojis_per_row)]
        owned_text = "Nothing Yet" if len(owned) == 0 else "\n".join(" ".join(row) for row in owned_rows)
        
        not_owned_rows = [not_owned[i:i + emojis_per_row] for i in range(0, len(not_owned), emojis_per_row)]
        not_owned_text = "\n".join(" ".join(row) for row in not_owned_rows)
        
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        embed.add_field(name="__Owned TestBalls__", value=owned_text, inline=False)
        embed.add_field(name=("__:tada: No missing countryball, congratulations! :tada:__" if len(owned) / len(emojis) == 1 else "__Missing TestBalls__"), value=not_owned_text, inline=False)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(CompletionCog(bot))