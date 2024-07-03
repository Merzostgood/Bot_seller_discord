import discord, sys
from datetime import datetime
sys.path.append("..")
from cogs.Db import reader, JSONUpdate

async def msg_purs(interaction, channel):
    database = await reader()
    role = discord.utils.get(interaction.guild.roles,
                      id=database[str(interaction.guild.id)]["settings"]['sellerRole'])

    embed = discord.Embed(title=f"{interaction.user.name} - купил товар(ы)",
                          colour=0xa3ff66,
                          timestamp=datetime.now())

    cart = ""
    i = 1


    for id, amount in database[str(interaction.user.guild.id)]["cart"][str(interaction.user.id)].items():
        product = database[str(interaction.user.guild.id)]["products"][int(id)][0]
        cost = database[str(interaction.user.guild.id)]["products"][int(id)][2]
        print(product, cost)
        temp = str(i) + ". " + product + " - " + str(amount) + "шт. " + "\n"
        cart = cart + temp
        i += 1

    embed.add_field(name="",
                    value=cart,
                    inline=False)

    embed.set_image(url="https://cdn.discordapp.com/attachments/1226424309514240000/1244946924709351474/png.png?ex=6656f6ac&is=6655a52c&hm=a68ec3e4698a4aa60a177e55c58663fe1c203c12e2fb484c94edf01c533c81b6&")

    embed.set_footer(text="By real. bot",
                     icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")

    channekl = discord.utils.get(interaction.guild.channels,
                             id=channel)

    ids = []
    for id, amount in database[str(interaction.user.guild.id)]["cart"][str(interaction.user.id)].items():
        ids.append(str(id))
    for i in ids:
        del database[str(interaction.user.guild.id)]["cart"][str(interaction.user.id)][i]

    database[str(interaction.user.guild.id)]["settings"]["channels"] += 1
    await JSONUpdate(database)

    await channekl.send(f"||{role.mention},{interaction.user.mention}||", embed=embed, view=Zakaz())

class Zakaz(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="  Выполнено  ", emoji="✅", custom_id="polyvinyl", row=0, style=discord.ButtonStyle.green)
    async def vipolnino_callback(self, button, interaction):
        database = await reader()

        await interaction.response.defer()
        msg = await interaction.original_response()
        role = discord.utils.get(interaction.guild.roles,
                                 id=database[str(interaction.guild.id)]["settings"]['sellerRole'])
        if role in interaction.user.roles:
            embed = discord.Embed(title="Вы уверены что хотите удалить тикет?",
                                  colour=0xf50000)
            embed.set_footer(text="By real. bot",
                             icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")
            await interaction.respond(embed=embed, ephemeral=True, view=YeNo(msg))

class YeNo(discord.ui.View):
    def __init__(self, msg):
        super().__init__(timeout=9999999)
        self.msg = msg

    @discord.ui.button(label="  Да ✅  ", row=0, style=discord.ButtonStyle.green)
    async def thgf_button_callback(self, button, interaction):
        await interaction.response.defer()
        database = await reader()
        channel = discord.utils.get(interaction.guild.channels,
                                    id=self.msg.channel.id)
        if database[str(interaction.user.guild.id)]["settings"]["log"] == "Yes":
            category = discord.utils.get(interaction.guild.categories,
                                        id=database[str(interaction.user.guild.id)]["settings"]["categoryLog"])

            for key, value in channel.overwrites.items():
                if key == interaction.guild.default_role:
                    pass
                else:
                    await channel.set_permissions(key, overwrite=None)
            await self.msg.edit(view=RemoveChannel())
            await channel.edit(category=category,
                               reason="Закрытие тикета")
        else:
            for key, value in channel.overwrites.items():
                if key == interaction.guild.default_role:
                    pass
                else:
                    await channel.set_permissions(key, overwrite=None)

            await channel.delete(reason="Закрытие тикета без включенных логов")

    @discord.ui.button(label="  Нет ❌  ", row=0, style=discord.ButtonStyle.red)
    async def fdst_button_callback(self, button, interaction):
        await interaction.response.defer()
        msg = await interaction.original_response()
        await msg.edit(delete_after=0.00001)

class RemoveChannel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="  Удалить канал  ", custom_id="remove", emoji='❌', row=0, style=discord.ButtonStyle.red)
    async def removel_callback(self, button, interaction):
        await interaction.response.defer()
        msg = await interaction.original_response()
        channel = discord.utils.get(interaction.guild.channels,
                                    id=msg.channel.id)
        await channel.delete(reason="Окончательное удаление канала")