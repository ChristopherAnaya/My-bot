import discord
from Databases.databases import load_data
cursor, cursor2, _, _, _, _ = load_data()

def paginate(allballs, page=1):
    start_index = (page - 1) * 25
    end_index = page * 25
    return allballs[start_index:end_index]

class PageButton(discord.ui.Button):
    def __init__(self, label, page, allballs, disabled=False, style=discord.ButtonStyle.secondary):
        super().__init__(label=label, style=style, disabled=disabled)
        self.page = page
        self.allballs = allballs
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        current_page = self.view.page
        new_page = current_page + 1 if self.page == "next" else current_page - 1 if self.page == "previous" else 1 if self.page == "<<" else (len(self.allballs) + 24)//25
        if new_page == 1:
            self.view.children[1].disabled = True
            self.view.children[3].disabled = False
        elif new_page == (len(self.allballs) + 24)//25:
            self.view.children[3].disabled = True
            self.view.children[1].disabled = False
        else:
            self.view.children[3].disabled = False
            self.view.children[1].disabled = False  
        self.view.children[2].label = new_page
        self.view.children[1].label = new_page - 1 if new_page - 1 > 0 else "..."
        self.view.children[3].label = new_page + 1 if new_page + 1 <= (len(self.allballs) + 24)//25 else "..."
        
        paginated_balls = paginate(self.allballs, new_page)
        self.view.children[6].options = [
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
