import discord, sys
from datetime import datetime
sys.path.append("..")
from cogs.db import reader

async def changeProductCart(msg, interaction):
    database = await reader()
    ctx = interaction.user

    AllCost = 0
    cart = ""
    i = 1

    for id, amount in database[str(ctx.guild.id)]["cart"][str(ctx.id)].items():
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

        await msg.edit(embed=embed, view=None)

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
        await msg.edit(embed=embed)

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