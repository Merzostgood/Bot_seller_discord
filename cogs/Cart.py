import discord, sys
from datetime import datetime
sys.path.append("..")
from cogs.db import reader, JSONUpdate
from cogs.Updaters import changeProductCart

class CartView(discord.ui.View):
    def __init__(self, nowid, msg):
        super().__init__(timeout=9999999)
        self.nowid = nowid
        self.msg = msg
    @discord.ui.button(label="  Изменить кол-во товаров  ", emoji="🛒", custom_id="buy", row=0, style=discord.ButtonStyle.green)
    async def buy_callback(self, button, interaction):
        await interaction.response.send_modal(ModalCart(interaction, self.msg,title="Укажите номер товара"))

class ModalCart(discord.ui.Modal):
    def __init__(self, interaction, msg, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.msg = msg
        self.interaction = interaction

        self.add_item(discord.ui.InputText(label="Номер товара", style=discord.InputTextStyle.short, max_length=2, placeholder="Введите номер товара в корзине. Например: 3"))
        self.add_item(discord.ui.InputText(label="Количесво", style=discord.InputTextStyle.short, max_length=2, placeholder="Введите количество товара в корзине. 0 - чтобы убрать из корзины"))

    async def callback(self, interaction: discord.Interaction):
        database = await reader()
        ctx = interaction.user
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
                            await changeProductCart(self.msg, self.interaction)
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
                            await changeProductCart(self.msg, self.interaction)
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