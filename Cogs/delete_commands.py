import discord
from discord.ext import commands
from discord import app_commands
from Databases.databases import load_data
cursor, _, cursor3, conn, _, conn3 = load_data()

class DeleteCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="delete", description="Deletes all your data")
    async def delete(self, interaction: discord.Interaction):
        view = ConfirmView(self, interaction.user)
        await interaction.response.send_message("This will delete all of your data are you sure you want to do this?", view=view, ephemeral=True)
            
class ConfirmView(discord.ui.View):
    def __init__(self, cog, user):
        super().__init__()
        self.cog = cog
        self.user = user

    @discord.ui.button(label="<:Check:1306356029554032669>", style=discord.ButtonStyle.green)#add cutom emoji these ones purple
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            child.disabled = True
        cursor.execute("DELETE FROM catches WHERE user_id = ?", (self.user.id,))
        cursor3.execute("DELETE FROM user_data WHERE user_id = ?", (self.user.id,))
        conn.commit()
        conn3.commit()
        await interaction.response.edit_message(content="All data deleted.", view=self)
        self.stop()
        

    @discord.ui.button(label="<:X_:1306356011887497216>", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(content="The action has been cancelled.", view=self)
        self.stop()

async def setup(bot):
    if bot.tree.get_command("delete"):
        bot.tree.remove_command("delete")
    await bot.add_cog(DeleteCommand(bot))