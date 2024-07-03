import discord, sys
from datetime import datetime
sys.path.append("..")
from cogs.Db import reader, JSONUpdate
from cogs.Updaters import changeProduct

class ProductsView(discord.ui.View):
    def __init__(self, nowid):
        super().__init__(timeout=9999999)
        self.nowid = nowid

    @discord.ui.button(row=0, emoji="◀", custom_id="prev", style=discord.ButtonStyle.secondary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.defer()
        msg = await interaction.original_response()
        if self.nowid > 0:
            self.nowid -= 1
            await changeProduct(self.nowid, interaction)

    @discord.ui.button(label="  Добавить в корзину  ", emoji="🛒", custom_id="buy", row=0, style=discord.ButtonStyle.green)
    async def buy_callback(self, button, interaction):
        await interaction.response.send_modal(Amount(self.nowid, title="Укажите количество товара в вашей корзине"))

    @discord.ui.button(label="", emoji="▶",row=0, custom_id="next", style=discord.ButtonStyle.secondary)
    async def last_button_callback(self, button, interaction):
        database = await reader()
        await interaction.response.defer()
        msg = await interaction.original_response()
        if len(database[str(interaction.user.guild.id)]) > self.nowid:
            self.nowid += 1
            await changeProduct(self.nowid, interaction)

class Amount(discord.ui.Modal):
    def __init__(self, nowid, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.id = nowid

        self.add_item(discord.ui.InputText(label="Количесво", style=discord.InputTextStyle.short, max_length=2, placeholder="Введите количество товара в корзине. Например: 3"))

    async def callback(self, interaction: discord.Interaction):
        try:
            database = await reader()
            ctx = interaction.user

            value = int(self.children[0].value)
            embed = discord.Embed(description=f"Теперь в корзине этого товара: {value}",
                                  colour=0x9ff500,
                                  timestamp=datetime.now())
            embed.set_author(name="✅ Успех!")
            embed.set_footer(text="By real. bot",
                             icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")

            database[str(interaction.guild.id)]["cart"][str(ctx.id)][str(self.id)] = value
            await JSONUpdate(database)
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=60)

        except:

            embed = discord.Embed(description="Вы должны указать **число**!",
                              colour=0xff0000,
                              timestamp=datetime.now())
            embed.set_author(name="❌ Ошибка")
            embed.set_footer(text="By real. bot",
                         icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")

            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=60)