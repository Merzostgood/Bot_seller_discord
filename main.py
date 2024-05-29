from discord.ext import commands
from discord.ui import Button
from datetime import datetime
from conf import TOKEN
import discord, random, string, time, json
bot = discord.Bot(debug_guilds=[1168481058031931422])

async def JSONUpdate(data):
    with open("database.json", "w") as f:
        f.write(json.dumps(data, indent=4))
    f.close()
    return data

async def reader():
    with open("database.json", "r") as f:
        data = json.loads(f.read())
    f.close()
    return data
@bot.event
async def on_ready():
    print("Satrt")

class Amount(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Количесво"))

    async def callback(self, interaction: discord.Interaction):
        try:
            value = int(self.children[0].value)
            embed = discord.Embed(description=f"Теперь в корзине этого товара: {value}",
                                  colour=0x9ff500,
                                  timestamp=datetime.now())
            embed.set_author(name="✅ Успех!")
            embed.set_footer(text="By real. bot",
                             icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")

            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=60)

        except:

            embed = discord.Embed(description="Вы должны указать **число**!",
                              colour=0xff0000,
                              timestamp=datetime.now())
            embed.set_author(name="❌ Ошибка")
            embed.set_footer(text="By real. bot",
                         icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")

            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=60)

class BuyMenu(discord.ui.View):
    def __init__(self, code, msg):
        super().__init__(timeout=9999999)
        self.code = code
        self.msg = msg

    @discord.ui.button(label="  Оплатил ✅  ", row=0, style=discord.ButtonStyle.green)
    async def first_button_callback(self, button, interaction):
        await interaction.response.defer()
        database = await reader()
        self.disable_all_items()
        Buyed = True
        Category = discord.utils.get(interaction.user.guild.categories, id=database[str(interaction.user.guild.id)]["settings"]["categoryid"])

        if Buyed == True:
            channel = await interaction.user.guild.create_text_channel(f'Purchase-{database[str(interaction.user.guild.id)]["settings"]["channels"]}', category=Category)
            database[str(interaction.user.guild.id)]["settings"]["channels"] += 1
            await JSONUpdate(database)

        time.sleep(2)
        self.enable_all_items()
        print("Check", self.code)

    @discord.ui.button(label="  Отмена ❌  ", row=0, style=discord.ButtonStyle.danger)
    async def second_button_callback(self, button, interaction):
        await interaction.response.defer()
        database = await reader()
        msg = self.msg
        nowid = 0
        guild = interaction.user.guild.id
        embed = discord.Embed(
            title=f"Товар - {database[str(guild)]['products'][nowid][0]} [{nowid + 1}/{len(database[str(guild)]['products'])}]",
            colour=0xadff5c,
            timestamp=datetime.now())
        embed.add_field(name="",
                             value=database[str(guild)]['products'][nowid][1],
                             inline=False)
        embed.add_field(name=f"Цена - {database[str(guild)]['products'][nowid][2]} алмазов",
                             value="",
                             inline=False)
        embed.set_image(
            url=database[str(guild)]['products'][nowid][3])
        embed.set_footer(text="By real. bot",
                              icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")
        await msg.edit(embed=embed, view=ProductsView(0,msg,embed, self.author))

async def changeProduct(nowid, msg, interaction):
    database = await reader()
    guild = interaction.user.guild.id
    embed = discord.Embed(
        title=f"Товар - {database[str(guild)]['products'][nowid][0]} [{nowid + 1}/{len(database[str(guild)]['products'])}]",
        colour=0xadff5c,
        timestamp=datetime.now())
    embed.add_field(name="",
                         value=database[str(guild)]['products'][nowid][1],
                         inline=False)
    embed.add_field(name=f"Цена - {database[str(guild)]['products'][nowid][2]} алмазов",
                         value="",
                         inline=False)
    embed.set_image(
        url=database[str(guild)]['products'][nowid][3])
    embed.set_footer(text="By real. bot",
                          icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")
    await msg.edit(embed=embed)


class ProductsView(discord.ui.View):
    def __init__(self, nowid, msg, embed):
        super().__init__(timeout=9999999)
        self.nowid = nowid
        self.msg = msg
        self.embed = embed

    @discord.ui.button(row=0, emoji="◀", custom_id="prev", style=discord.ButtonStyle.secondary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.defer()
        if self.nowid > 0:
            self.nowid -= 1
            await changeProduct(self.nowid, self.msg, interaction)

    @discord.ui.button(label="  Добавить в корзину  ", emoji="🛒", custom_id="buy", row=0, style=discord.ButtonStyle.green)
    async def buy_callback(self, button, interaction):
        await interaction.response.send_modal(Amount(title="Укажите количество товара в вашей корзине"))

    @discord.ui.button(label="", emoji="▶",row=0, custom_id="next", style=discord.ButtonStyle.secondary)
    async def last_button_callback(self, button, interaction):
        database = await reader()
        await interaction.response.defer()
        if len(database[str(interaction.user.guild.id)]) > self.nowid:
            self.nowid += 1
            await changeProduct(self.nowid, self.msg, interaction)


# COMMANDS

@bot.slash_command()
@discord.default_permissions(
    administrator=True
)
async def product_add(ctx: discord.ApplicationContext):
    await ctx.respond(f"Hello {ctx.author}, you are an administrator.")

@bot.slash_command()
async def products(ctx: discord.ApplicationContext):
    database = await reader()
    guild = ctx.guild.id
    embed = discord.Embed(title=f"Товар - {database[str(guild)]['products'][0][0]} [1/{len(database[str(guild)]['products'])}]",
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
    embed.set_footer(text="By real. bot",
                     icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")

    msg = await ctx.respond(embed=embed, ephemeral=True)
    await msg.edit(embed=embed, view=ProductsView(0, msg, embed))


@bot.slash_command()
async def test_sold(ctx: discord.ApplicationContext):
    database = await reader()
    role = discord.utils.get(ctx.guild.roles,
                      id=database[str(ctx.guild.id)]["settings"]['sellerRole'])

    embed = discord.Embed(title=f"metiopn - купил товар(ы)",
                          colour=0xa3ff66,
                          timestamp=datetime.now())

    embed.add_field(name="",
                    value="{ товар } - { количество } штук\n{ товар2 } - { количество2 } штук\n{ товар3 } - { количество3 } штук",
                    inline=False)

    embed.set_image(url="https://cdn.discordapp.com/attachments/1226424309514240000/1244946924709351474/png.png?ex=6656f6ac&is=6655a52c&hm=a68ec3e4698a4aa60a177e55c58663fe1c203c12e2fb484c94edf01c533c81b6&")

    embed.set_footer(text="By real. bot",
                     icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")

    msg = await ctx.respond(f"||{role.mention}||",embed=embed)

bot.run(TOKEN)
