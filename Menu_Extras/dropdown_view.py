import discord
from discord.ui import View
from Menu_Extras import Dropdown, QuitButton, PageButton
from Menu_Extras.Buttons.current_button import CurrentButton

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
            #put cutom age number here
            self.add_item(Dropdown(allballs, page))
