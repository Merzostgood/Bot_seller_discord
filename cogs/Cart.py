import discord, sys, random, string, time
from datetime import datetime
sys.path.append("..")
from cogs.db import reader, JSONUpdate
from cogs.Updaters import changeProductCart
from cogs.purchases import msg_purs

class DeleteAll(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=9999999)

    @discord.ui.button(label="  Да ✅  ", row=0, style=discord.ButtonStyle.green)
    async def thgf_button_callback(self, button, interaction):
        await interaction.response.defer()
        msg = await interaction.original_response()
        database = await reader(); ids = []

        for id, amount in database[str(interaction.user.guild.id)]["cart"][str(interaction.user.id)].items():
            ids.append(str(id))
        for i in ids:
            del database[str(interaction.user.guild.id)]["cart"][str(interaction.user.id)][i]
        await JSONUpdate(database)

        await changeProductCart(interaction)


    @discord.ui.button(label="  Нет ❌  ", row=0, style=discord.ButtonStyle.red)
    async def fdst_button_callback(self, button, interaction):
        await interaction.response.defer()
        msg = await interaction.original_response()
        await msg.edit(view=CartView())
        await changeProductCart(interaction)


class CartView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=9999999)

    @discord.ui.button(label="  Изменить кол-во товаров  ", emoji="🛒", row=0, style=discord.ButtonStyle.secondary)
    async def buy_callback(self, button, interaction):
        await interaction.response.send_modal(ModalCart(interaction, title="Укажите номер товара"))

    @discord.ui.button(label="  Очистить корзину  ", emoji="❌", row=0, style=discord.ButtonStyle.red)
    async def b_callback(self, button, interaction):
        await interaction.response.defer()
        embed = discord.Embed(title="Вы уверены что хотите удалить  все товары с корзины?",
                              colour=0xff5252)
        embed.set_footer(text="By real. bot",
                         icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")

        msg = await interaction.original_response()
        await msg.edit(embed=embed, view=DeleteAll())

    @discord.ui.button(label="  Оплатить  ", emoji="✅", row=0, style=discord.ButtonStyle.green)
    async def oplata_callback(self, button, interaction):
        database = await reader()
        allcost = 0
        await interaction.response.defer()

        for id, amount in database[str(interaction.user.guild.id)]["cart"][str(interaction.user.id)].items():
            allcost += database[str(interaction.user.guild.id)]["products"][int(id)][2] * amount

        if allcost <= 1728:
            await oplata(interaction, allcost)
        else:
            embed = discord.Embed(description="_Максимальная общая_ стоимость товаров 1728 алмазов!",
                                  colour=0xff0000,
                                  timestamp=datetime.now())
            embed.set_author(name="❌ Ошибка")
            embed.set_footer(text="By real. bot",
                             icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")

            await interaction.respond(embed=embed, ephemeral=True, delete_after=10)



class ModalCart(discord.ui.Modal):
    def __init__(self, interaction, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.interaction = interaction

        self.add_item(discord.ui.InputText(label="Номер товара", style=discord.InputTextStyle.short, max_length=2, placeholder="Введите номер товара в корзине. Например: 3"))
        self.add_item(discord.ui.InputText(label="Количесво", style=discord.InputTextStyle.short, max_length=2, placeholder="Введите количество товара в корзине. 0 - чтобы убрать из корзины"))

    async def callback(self, interaction: discord.Interaction):
        database = await reader()
        ctx = interaction.user
        await interaction.response.defer()
        msg = await interaction.original_response()
        try:
            value2 = int(self.children[1].value)
            value = int(self.children[0].value)
            if value <= len(database[str(interaction.user.guild.id)]["cart"][str(interaction.user.id)]):
                if value2 == 0:
                    i = 1
                    for id, amount in database[str(ctx.guild.id)]["cart"][str(ctx.id)].items():
                        if i == value:
                            del database[str(ctx.guild.id)]["cart"][str(ctx.id)][str(id)]
                            embed = discord.Embed(description=f"Больше в корзине нету {value} товара.",
                                                  colour=0x9ff500,
                                                  timestamp=datetime.now())
                            embed.set_author(name="✅ Успех!")
                            embed.set_footer(text="By real. bot",
                                             icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")
                            await JSONUpdate(database)
                            await changeProductCart(self.interaction)
                            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=10)
                        else:
                            i+=1
                else:
                    i = 1
                    for id, amount in database[str(ctx.guild.id)]["cart"][str(ctx.id)].items():
                        if i == value:
                            database[str(ctx.guild.id)]["cart"][str(ctx.id)][str(id)] = value2
                            embed = discord.Embed(description=f"Теперь в корзине {value} товара: {value2}",
                                                      colour=0x9ff500,
                                                      timestamp=datetime.now())
                            embed.set_author(name="✅ Успех!")
                            embed.set_footer(text="By real. bot",
                                                 icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")
                            await JSONUpdate(database)
                            await changeProductCart(self.interaction)
                            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=10)
                        else:
                            i += 1
            else:
                embed = discord.Embed(description="Проверьте правильность товара в корзине!",
                                      colour=0xff0000,
                                      timestamp=datetime.now())
                embed.set_author(name="❌ Ошибка")
                embed.set_footer(text="By real. bot",
                                 icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")

                await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=10)
        except:
            embed = discord.Embed(description="Все поля должны быть числами!!",
                                  colour=0xff0000,
                                  timestamp=datetime.now())
            embed.set_author(name="❌ Ошибка")
            embed.set_footer(text="By real. bot",
                             icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")

            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=10)

# Oplata

class BuyMenu(discord.ui.View):
    def __init__(self, code):
        super().__init__(timeout=999)
        self.code = code

    @discord.ui.button(label="  Оплатил ✅  ", row=0, style=discord.ButtonStyle.green)
    async def first_button_callback(self, button, interaction):
        await interaction.response.defer()
        database = await reader()
        self.disable_all_items()
        Category = discord.utils.get(interaction.user.guild.categories, id=database[str(interaction.user.guild.id)]["settings"]["categoryid"])


        if Category:
            channel = await interaction.user.guild.create_text_channel(f'purchase-{database[str(interaction.user.guild.id)]["settings"]["channels"]}', category=Category)
            await channel.set_permissions(interaction.user, send_messages=True, read_message_history=False,
                                          read_messages=True)

        self.enable_all_items()
        msg = await interaction.original_response()
        await msg.edit(delete_after=0.1)
        await msg_purs(interaction, channel.id)

    @discord.ui.button(label="  Отмена ❌  ", row=0, style=discord.ButtonStyle.danger)
    async def second_button_callback(self, button, interaction):
        await interaction.response.defer()
        msg = await interaction.original_response()
        await msg.edit(view=CartView())
        await changeProductCart(interaction)


async def oplata(interaction, cost):
    msg = await interaction.original_response()
    code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7))

    embed = discord.Embed(
        title="",
        colour=0xadff5c,
        timestamp=datetime.now())
    embed.add_field(name="Оплата ✅",
                    value=f"Переведите adamcowell14 - {cost} алмазов, при этом обязательно добавьте комментарий - {code}.",
                    inline=False)

    embed.set_footer(text="By real. bot",
                     icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")

    await msg.edit(embed=embed, view=BuyMenu(code))