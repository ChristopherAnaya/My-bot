import discord
from discord.ui import Modal, TextInput, Button, View

class UserInfoModal(Modal):
    def __init__(self, view, button):
        super().__init__(title="Catch This Testball!")
        self.button = button
        self.view = view
        self.name_input = TextInput(label="Name Of This Ball", placeholder="Your Guess")
        self.add_item(self.name_input)
    async def on_submit(self, interaction: discord.Interaction):
        name = (self.name_input.value).strip().title()
        await interaction.response.send_message(f"{interaction.user.mention} I was caught already!")
        await interaction.response.send_message(f"{interaction.user.mention} You caught **{name}!** `(#fewf, wfeewf)`")
        await interaction.message.edit(view=self.view)

