from datetime import datetime
from conf import TOKEN
from cogs.db import reader, JSONUpdate
from cogs.Cart import CartView
from cogs.Products import ProductsView
from cogs.Updaters import newUser
from cogs.purchases import Zakaz
import discord
bot = discord.Bot(debug_guilds=[1168481058031931422,1216358724961177630])


@bot.event
async def on_ready():
    print("Satrt")
    database = await reader()
    bot.add_view(Zakaz())


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

bot.run(TOKEN)
