import discord

class QuitButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Quit", style=discord.ButtonStyle.danger)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        for child in self.view.children:
            child.disabled = True
        await interaction.edit_original_response(view=self.view)