from discord.ext import commands
from discord.ui import Button
from datetime import datetime
import discord, random, string
bot = discord.Bot(debug_guilds=[1168481058031931422])


@bot.slash_command()
@discord.default_permissions(
    administrator=True
)
async def product_add(ctx: discord.ApplicationContext):
    await ctx.respond(f"Hello {ctx.author}, you are an administrator.")

database = {1168481058031931422:
                [["Плащ Маинкрафт Твитч1","описание 123123123\nописание 555",12345,"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQCuW30tbwC1akm8RHn7pB8Tz9U3vTRSTCAq6bAEWqp3Q&s"],
                ["Плащ Маинкрафт Твитч2","описание 123123123\nописание 555",1488,"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQCuW30tbwC1akm8RHn7pB8Tz9U3vTRSTCAq6bAEWqp3Q&s"],
                ["Плащ Маинкрафт Твитч3","описание 123123123\nописание 555",1488,"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQCuW30tbwC1akm8RHn7pB8Tz9U3vTRSTCAq6bAEWqp3Q&s"],
                ["Плащ Маинкрафт Твитч4","описание 123123123\nописание 555",1488,"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQCuW30tbwC1akm8RHn7pB8Tz9U3vTRSTCAq6bAEWqp3Q&s"]]}


class BuyMenu(discord.ui.View):
    def __init__(self, code, msg, author):
        super().__init__(timeout=9999999)
        self.code = code
        self.msg = msg
        self.author = author

    @discord.ui.button(label="  Оплатил ✅  ", row=0, style=discord.ButtonStyle.green)
    async def first_button_callback(self, button, interaction):
        await interaction.response.defer()
        print("Check", self.code)

    @discord.ui.button(label="  Отмена ❌  ", row=0, style=discord.ButtonStyle.danger)
    async def second_button_callback(self, button, interaction):
        await interaction.response.defer()
        msg = self.msg
        nowid = 0
        guild = interaction.user.guild.id
        embed = discord.Embed(
            title=f"Товар - {database[guild][nowid][0]} [{nowid + 1}/{len(database[guild])}]",
            colour=0xadff5c,
            timestamp=datetime.now())
        embed.add_field(name="",
                             value=database[guild][nowid][1],
                             inline=False)
        embed.add_field(name=f"Цена - {database[guild][nowid][2]} алмазов",
                             value="",
                             inline=False)
        embed.set_image(
            url=database[guild][nowid][3])
        await msg.edit(embed=embed, view=ProductsView(0,msg,embed, self.author))

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            return interaction.user.id == self.author.id
        else:
            embed = discord.Embed(description="Это сообщение не преднадлежит тебе.",
                                  colour=0xff0000,
                                  timestamp=datetime.now())
            embed.set_author(name="❌ Ошибка")
            embed.set_footer(text="By real. bot",
                             icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=60)

class ProductsView(discord.ui.View):
    def __init__(self, nowid, msg, embed, ctx):
        super().__init__(timeout=9999999)
        self.nowid = nowid
        self.msg = msg
        self.embed = embed
        self.author = ctx

    @discord.ui.button(label="  ⬅  ", row=0, custom_id="prev", style=discord.ButtonStyle.secondary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.defer()
        if self.nowid > 0:
            global database
            msg = self.msg
            guild = interaction.user.guild.id
            self.nowid = self.nowid - 1
            self.embed = discord.Embed(title=f"Товар - {database[guild][self.nowid][0]} [{self.nowid+1}/{len(database[guild])}]",
                                       colour=0xadff5c,
                                       timestamp=datetime.now())
            self.embed.add_field(name="",
                                 value=database[guild][self.nowid][1],
                                 inline=False)
            self.embed.add_field(name=f"Цена - {database[guild][self.nowid][2]} алмазов",
                                 value="",
                                 inline=False)
            self.embed.set_image(
                url=database[guild][self.nowid][3])
            await msg.edit(embed=self.embed)

    @discord.ui.button(label="  ✅ Купить товар  ", custom_id="buy", row=0, style=discord.ButtonStyle.green)
    async def buy_callback(self, button, interaction):
        await interaction.response.defer()
        msg = self.msg
        code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7))

        embed = discord.Embed(
            title="",
            colour=0xadff5c,
            timestamp=datetime.now())
        embed.add_field(name="Оплата ✅",
                        value=f"Переведите adamcowell14 - {database[interaction.user.guild.id][self.nowid][2]} алмазов, при этом обязательно добавьте комментарий - {code}",
                        inline=False)

        embed.set_footer(text="By real. bot",
                         icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")

        await msg.edit(embed=embed, view=BuyMenu(code, self.msg, self.author))

    @discord.ui.button(label="  ⮕  ", row=0, custom_id="next", style=discord.ButtonStyle.secondary)
    async def last_button_callback(self, button, interaction):
        global database
        await interaction.response.defer()
        if len(database[interaction.user.guild.id]) > self.nowid:
            msg = self.msg
            guild = interaction.user.guild.id
            self.nowid = self.nowid + 1
            self.embed = discord.Embed(title=f"Товар - {database[guild][self.nowid][0]} [{self.nowid+1}/{len(database[guild])}]",
                                       colour=0xadff5c,
                                       timestamp=datetime.now())
            self.embed.add_field(name="",
                                 value=database[guild][self.nowid][1],
                                 inline=False)
            self.embed.add_field(name=f"Цена - {database[guild][self.nowid][2]} алмазов",
                                 value="",
                                 inline=False)
            self.embed.set_image(
                url=database[guild][self.nowid][3])
            await msg.edit(embed=self.embed)
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            return interaction.user.id == self.author.id
        else:
            embed = discord.Embed(description="Это сообщение не преднадлежит тебе.",
                              colour=0xff0000,
                              timestamp=datetime.now())
            embed.set_author(name="❌ Ошибка")
            embed.set_footer(text="By real. bot",
                         icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=60)

@bot.slash_command()
async def products(ctx: discord.ApplicationContext):
    global database
    nowid = 0
    guild = ctx.guild.id
    embed = discord.Embed(title=f"Товар - {database[guild][nowid][0]} [{nowid+1}/{len(database[guild])}]",
                          colour=0xadff5c,
                          timestamp=datetime.now())
    embed.add_field(name="",
                    value=database[guild][nowid][1],
                    inline=False)
    embed.add_field(name=f"Цена - {database[guild][nowid][2]} алмазов",
                    value="",
                    inline=False)
    embed.set_image(
        url=database[guild][nowid][3])
    embed.set_footer(text="By real. bot",
                     icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")

    msg = await ctx.respond(embed=embed)
    await msg.edit(embed=embed, view=ProductsView(nowid, msg, embed, ctx.author))


bot.run("token")
