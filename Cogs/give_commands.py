import discord
from discord.ext import commands
from discord import app_commands
from Databases.databases import load_data
cursor, cursor2, _, conn, _, _ = load_data()

class GiveCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="give", description="Give me ur balls lil bro")
    @app_commands.describe(ball="The ball")
    @app_commands.describe(user="The user whose TestBalls you want to view (mention or ID)")
    async def give(self, interaction: discord.Interaction, ball: str, user: discord.User):
        ball = "".join([s.replace("🤍", "") for s in ball])
        ball = ball.split()
        print(ball)
        if not cursor.execute('SELECT * FROM catches WHERE user_id = ? AND catch_name = ? AND catch_id = ?', (interaction.user.id, ball[1], ball[0][1:])).fetchone():
            await interaction.response.send_message("The Testball Could Not Be Found", ephemeral = True)
        elif interaction.user == user:
            await interaction.response.send_message("You cannot give a testball to yourself.")
        else:
            cursor.execute('UPDATE catches SET past_owner = ?, user_id = ?, favorite = ? WHERE catch_name = ? AND catch_id = ?', (interaction.user.id, user.id, 0, ball[1], ball[0][1:]))
            conn.commit()
            await interaction.response.send_message(f"You just gave the testball{cursor2.execute('SELECT * FROM ball_data WHERE ball_name = ?', (ball[1],)).fetchone()[1]}{ball[0]} {ball[1]} (`{ball[2][4:]}/{ball[3][3:]}`) to <@{user.id}>")

                
    @give.autocomplete("ball")
    async def autocomplete_callback(self, interaction: discord.Interaction, current: str):
        ball_options = cursor.execute('SELECT * FROM catches WHERE user_id = ?', (interaction.user.id,)).fetchall()
        suggestions = [f"{"🤍" if ball[6] == 1 else ""}#{ball[2]} {ball[1]} ATK:{("+" if int(ball[3]) >= 0 else "") + ball[3]}% HP:{("+" if int(ball[4]) >= 0 else "") + ball[4]}%" for ball in ball_options]
        filtered_suggestions = [s for s in suggestions if current.lower() in s.lower()][:25]
        return [
            app_commands.Choice(name=suggestion, value=suggestion) for suggestion in filtered_suggestions
        ]

async def setup(bot):
    if bot.tree.get_command("give"):
        bot.tree.remove_command("give")
    await bot.add_cog(GiveCommand(bot))