from datetime import datetime
from conf import TOKEN
from cogs.Db import reader, JSONUpdate
from cogs.Cart import CartView
from cogs.Products import ProductsView
from cogs.Updaters import newUser
from cogs.Purchases import Zakaz, RemoveChannel
from cogs.ProductManager import Sure, Edit, products_list
from discord import Option
import discord

bot = discord.Bot(debug_guilds=["Your guild id here"])
product = discord.SlashCommandGroup("product", "Math related commands", default_member_permissions=discord.Permissions(administrator=True))

@bot.event
async def on_ready():
    bot.add_view(Zakaz())
    bot.add_view(RemoveChannel())

# COMMANDS
@product.command()
async def add(ctx: discord.ApplicationContext,
                      name: Option(str, required=True, max_length=32),
                      description: Option(str, required=True, max_length=128),
                      price: Option(int, required=True, max_value=1728),
                      image: Option(discord.Attachment, required=True)):
    await ctx.response.defer()
    whitelist = ['image/webp', 'image/jpeg', 'image/gif', 'image/png']
    if image.content_type in whitelist:
        embed = discord.Embed(
            title=f"**Пример как будет выглядить товар : **\nТовар - {name}",
            colour=0xadff5c,
            timestamp=datetime.now())
        embed.add_field(name="",
                        value=description,
                        inline=False)
        embed.add_field(name=f"Цена - {price} алмазов",
                        value="",
                        inline=False)
        embed.set_image(
            url=image.url)
        embed.set_footer(text="By Real bot",
                         icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")
        await ctx.respond(embed=embed, view=Sure([name, description, price, image.url]), ephemeral=True, delete_after=600)
    else:
        pass

@product.command()
async def remove(ctx: discord.ApplicationContext,
                 product_user: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(products_list))):
    await ctx.response.defer()
    database = await reader()
    for product in database[str(ctx.guild.id)]["products"]:
        if product[0] == product_user:
            database[str(ctx.guild.id)]["products"].remove(product)
            await JSONUpdate(database)
            embed = discord.Embed(description=f"",
                                  colour=0x9ff500,
                                  timestamp=datetime.now())
            embed.set_author(name="✅ Успех!")
            embed.set_footer(text="By real. bot",
                             icon_url="https://cdn.discordapp.com/avatars/1198958063206539285/84ce6a1cd45596afc80656e6c5bfbb46.webp?size=128")
            await ctx.respond(embed=embed, delete_after=15, ephemeral=True)

@product.command()
async def edit(ctx: discord.ApplicationContext,
                 product_user: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(products_list))):
    await ctx.response.defer()
    database = await reader()
    for product in database[str(ctx.guild.id)]["products"]:
        if product[0] == product_user:
            guild = ctx.guild.id
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

            await ctx.respond(embed=embed, view=Edit(), ephemeral=True, delete_after=600)

@bot.slash_command()
async def products(ctx: discord.ApplicationContext):
    database = await reader()

    try:
        val = database[str(ctx.guild.id)]["cart"][str(ctx.author.id)]
    except:
        await newUser(ctx)

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

    await ctx.respond(embed=embed, view=ProductsView(0), ephemeral=True)

@bot.slash_command()
async def cart(ctx: discord.ApplicationContext):
    database = await reader()

    try:
        val = database[str(ctx.guild.id)]["cart"][str(ctx.author.id)]
    except:
        await newUser(ctx)

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

        await ctx.respond(embed=embed, view=CartView(), ephemeral=True, delete_after=600)

bot.add_application_command(product)
bot.run(TOKEN)
