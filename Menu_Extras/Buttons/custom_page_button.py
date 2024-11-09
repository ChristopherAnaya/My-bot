import discord
from Databases.databases import load_data
from discord.ui import Modal, TextInput, Button, View

_, cursor2, _, _, _, _ = load_data()

def paginate(allballs, page=1):
    start_index = (page - 1) * 15
    end_index = page * 15
    return allballs[start_index:end_index]




        








class CustomPageButton(discord.ui.Button):
    def __init__(self, allballs):
        super().__init__(label="Skip To Page...", style=discord.ButtonStyle.secondary)
        self.allballs = allballs
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        new_page = int(2)#place holder for modal
        
        
        if new_page == 1:
            self.view.children[1].disabled = True
            self.view.children[3].disabled = False
        elif new_page == (len(self.allballs) + 14)//15:
            self.view.children[3].disabled = True
            self.view.children[1].disabled = False
        else:
            self.view.children[3].disabled = False
            self.view.children[1].disabled = False  
        self.view.children[2].label = new_page
        self.view.children[1].label = new_page - 1 if new_page - 1 > 0 else "..."
        self.view.children[3].label = new_page + 1 if new_page + 1 <= (len(self.allballs) + 14)//15 else "..."
        
        paginated_balls = paginate(self.allballs, new_page)
        self.view.children[7].options = [
            discord.SelectOption(
                label=f"#{x[2]} {x[1]}",
                description=f"ATK: {int(int(cursor2.execute('SELECT * FROM ball_data WHERE ball_name = ?', (x[1],)).fetchone()[2]) * (int(x[3].split(':')[0]) / 100 + 1 ))} " \
                            f"({'+' if x[3].split(':')[0][0] != '-' else ''}{str(int(x[3].split(':')[0]))}%)∙" \
                            f"HP: {int(int(cursor2.execute('SELECT * FROM ball_data WHERE ball_name = ?', (x[1],)).fetchone()[3]) * (int(x[3].split(':')[1]) / 100 + 1 ))} " \
                            f"({'+' if x[3].split(':')[1][0] != '-' else ''}{str(int(x[3].split(':')[1]))}%)",
                emoji=cursor2.execute('SELECT * FROM ball_data WHERE ball_name = ?', (x[1],)).fetchone()[1]
            )
            for x in paginated_balls
        ]
        await interaction.edit_original_response(view=self.view)