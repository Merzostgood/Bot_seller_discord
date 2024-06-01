from discord.ext import commands
from discord.ui import Button
from datetime import datetime
from conf import TOKEN
from cogs.db import reader, JSONUpdate
from cogs.Cart import CartView
from cogs.Products import ProductsView
import discord, random, string, time, json
bot = discord.Bot(debug_guilds=[1168481058031931422])


@bot.event
async def on_ready():
    print("Satrt")

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
        await msg.edit(embed=embed, view=ProductsView(0, msg))



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
    await msg.edit(embed=embed, view=ProductsView(0, msg))


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

    msg = await ctx.respond(f"||{role.mention}||", embed=embed)

@bot.slash_command()
async def cart(ctx: discord.ApplicationContext):
    database = await reader()

    AllCost = 0
    cart = ""
    i = 1


    for id, amount in database[str(ctx.guild.id)]["cart"][str(ctx.user.id)].items():
        product = database[str(ctx.guild.id)]["products"][int(id)][0]
        cost = database[str(ctx.guild.id)]["products"][int(id)][2]
        print(product, cost)
        temp = str(i) + ". " + product + " - " + str(amount) + "шт., " + str(cost * amount) + " алмазов." + "\n"
        cart = cart + temp
        AllCost += cost * amount
        i += 1

    if i == 1:
        embed = discord.Embed(timestamp=datetime.now())
        embed.add_field(name="🛒 **Ваша корзина**",
                        value="Ваша корзина пустая! Зайдите в магазин чтобы купить что-то /products",
                        inline=True)
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1226424309514240000/1245294823422824508/cart.png?ex=66583aae&is=6656e92e&hm=c9b52113dd06ab0badffcfdd1b63687ee088c8b1b1366fccc57c230eaac47e29&")
        embed.set_footer(text="By real. bot",
                         icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")

        await ctx.respond(embed=embed, ephemeral=True, delete_after=600)

    else:
        embed = discord.Embed(timestamp=datetime.now())
        embed.add_field(name="🛒 **Ваша корзина**",
                        value=cart,
                        inline=True)
        embed.add_field(name=f"🔹 Общая стоимость - {AllCost} алмазов.",
                        value="",
                        inline=False)
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1226424309514240000/1245294823422824508/cart.png?ex=66583aae&is=6656e92e&hm=c9b52113dd06ab0badffcfdd1b63687ee088c8b1b1366fccc57c230eaac47e29&")
        embed.set_footer(text="By real. bot",
                         icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")
        msg = await ctx.respond(embed=embed, ephemeral=True, delete_after=600)
        await msg.edit(embed=embed, view=CartView(1, msg))

bot.run(TOKEN)
