from datetime import datetime
from cogs.Db import reader, JSONUpdate
import discord


async def ErrorEmbed(reason):
    embed = discord.Embed(description=reason,
                                  colour=0xff0000,
                                  timestamp=datetime.now())
    embed.set_author(name="❌ Ошибка")
    embed.set_footer(text="By Real bot",
                             icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")
    return embed

async def products_list(ctx: discord.AutocompleteContext):
    database = await reader(); products = []
    for product in database[str(ctx.interaction.user.guild.id)]["products"]: products.append(product[0])
    return products

class New(discord.ui.Modal):
    def __init__(self, choice, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.choice = choice

        self.add_item(discord.ui.InputText(label="Текст / число", style=discord.InputTextStyle.long))

    async def callback(self, interaction):

        await interaction.response.defer()

        database = await reader()
        msg = await interaction.original_response()
        value = self.children[0].value
        guild = interaction.guild.id
        updated = False


        if self.choice == 'Изменить имя товара':
            if len(value) <= 32:
                updated = True
                database[str(guild)]['products'][0][0] = value
            else:
                await interaction.response.send_message(embed=await ErrorEmbed('Имя товара не должно привышать 32 символов!'), ephemeral=True, delete_after=10)

        elif self.choice == 'Изменить описание товара':
            if len(value) <= 128:
                updated = True
                database[str(guild)]['products'][0][1] = value
            else:
                await interaction.response.send_message(embed=await ErrorEmbed('Описание товара не должно привышать 128 символов!'), ephemeral=True, delete_after=10)

        elif self.choice == 'Изменить цену товара':
            try:
                if int(value) <= 1728:
                    updated = True
                    database[str(guild)]['products'][0][2] = value
                else:
                    await interaction.response.send_message(embed=await ErrorEmbed('Цена товара не должна привышать 1728 алмазов!'), ephemeral=True, delete_after=10)
            except:
                await interaction.response.send_message(embed=await ErrorEmbed('Цена товара должна быть числом!'), ephemeral=True, delete_after=10)

        if updated:
            await JSONUpdate(database)
            embed = discord.Embed(
                title=f"**Пример как будет выглядить товар : **\nТовар - {database[str(guild)]['products'][0][0]}",
                colour=0xadff5c,
                timestamp=datetime.now())
            embed.add_field(name="",
                        value=database[str(guild)]["products"][0][1],
                        inline=False)
            embed.add_field(name=f"Цена - {database[str(guild)]['products'][0][2]} алмазов",
                        value="",
                        inline=False)
            embed.set_image(
                url=database[str(guild)]["products"][0][3])
            embed.set_footer(text="By Real bot",
                            icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")
            await msg.edit(embed=embed)

class Edit(discord.ui.View):
    @discord.ui.select(
        placeholder = "Изменить _ товара!",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="Изменить имя товара",
                description=""
            ),
            discord.SelectOption(
                label="Изменить описание товара",
                description=""
            ),
            discord.SelectOption(
                label="Изменить цену товара",
                description=""
            )
        ]
    )
    async def select_callback(self, select, interaction):
        await interaction.response.send_modal(New(choice=select.values[0], title="Введите новое название / описание / цену"))

class Sure(discord.ui.View):
    def __init__(self, settings):
        super().__init__(timeout=9999999)
        self.settings = settings

    @discord.ui.button(label="  Да  ", emoji="✅", row=0, style=discord.ButtonStyle.green)
    async def thgfd_button_callback(self, button, interaction):
        await interaction.response.defer()
        msg = await interaction.original_response()
        database = await reader()
        database[str(interaction.guild.id)]["products"].append(self.settings)
        await JSONUpdate(database)
        embed = discord.Embed(description=f"",
                              colour=0x9ff500,
                              timestamp=datetime.now())
        embed.set_author(name="✅ Успех!")
        embed.set_footer(text="By real. bot",
                         icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")
        await msg.edit(embed=embed, view=None, delete_after=15)

    @discord.ui.button(label="  Нет  ", emoji="❌", row=0, style=discord.ButtonStyle.red)
    async def fdsth_button_callback(self, button, interaction):
        await interaction.response.defer()
        msg = await interaction.original_response()
        await msg.edit(delete_after=0.00001)

