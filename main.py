from discord.ext import commands
from discord.ext.commands import bot

import base64
import json
import random
import discord, datetime, time
from discord.ext import commands
from discord.ext.commands import bot, clean_content
import requests

bot = commands.Bot(command_prefix='c!',
                   description="This is TDA BOT V2, better than the V1. This is so special because I coded it all myself!")

TOKEN = open("token.txt", "r").read()

STARTUP_MESSAGE = 'Ready'

bot.membercount_channel = bot.get_channel(823459333848563713)


@bot.event
async def on_ready():
    print(STARTUP_MESSAGE)
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name=" Dronesavia "))


@bot.command()
async def game(ctx):
    '''
    Sends the game link
    '''
    await ctx.send('https://roblox.com/games/5244574110/Dronesavia-Brand-New-RP')


@bot.command()
async def suggest(ctx, *, suggestion):
    """Suggestion command. Sends an suggestion to an channel."""
    await ctx.channel.purge(limit=1)
    channel = discord.utils.get(ctx.guild.text_channels, name='tda-bot-suggestions')
    suggestEmbed = discord.Embed(colour=0xFF0000)
    suggestEmbed.set_author(name=f'Suggested by {ctx.message.author}', icon_url=f'{ctx.author.avatar_url}')
    suggestEmbed.add_field(name='New suggestion!', value=f'{suggestion}')
    await channel.send(embed=suggestEmbed)


@bot.command()
async def throw(ctx):
    '''
    Mad? throw a table against people.
    '''
    await ctx.send("(╯°□°)╯︵ ┻━┻")


@bot.command()
async def members(ctx):
    '''
    Shows member count.
    '''
    await ctx.send(f"{ctx.guild.member_count}")


@bot.command()
async def kill(ctx, *, user='You'):
    '''
    Kills the player, minecraft style
    '''
    await ctx.send((user) + ' fell out of the world')


@bot.command()
async def choose(ctx, *choices: str):
    '''
    Picks randomly from all choices provided.
    '''
    await ctx.send((random.choice(choices)) + ', I choose you!')


@bot.command()
async def minecraft(ctx, username='Shrek'):
    '''
    Shows MC account info, skin and username history
    '''
    uuid = requests.get('https://api.mojang.com/users/profiles/minecraft/{}'
                        .format(username)).json()['id']

    url = json.loads(base64.b64decode(requests.get(
        'https://sessionserver.mojang.com/session/minecraft/profile/{}'
            .format(uuid)).json()['properties'][0]['value'])
                     .decode('utf-8'))['textures']['SKIN']['url']

    names = requests.get('https://api.mojang.com/user/profiles/{}/names'
                         .format(uuid)).json()
    history = "**Name History:**\n"
    for name in reversed(names):
        history += name['name'] + "\n"

    await ctx.send('**Username: `{}`**\n**Skin: {}**\n**UUID: {}**'.format(username, url, uuid))
    await ctx.send(history)


@bot.command()
async def userinfo(ctx, *, user: discord.Member = None):
    '''
    shows info about the user you pinged or yourself.
    '''
    if user is None:
        user = ctx.author
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(color=0xdfa3ff, description=user.mention)
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(user.roles) - 1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.add_field(name="Guild permissions", value=perm_string, inline=False)
    embed.set_footer(text='ID: ' + str(user.id))
    return await ctx.send(embed=embed)


@bot.command()
async def ping(ctx):
    '''
    Shows bots ping
    '''
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping)}ms`")
    print(f'Ping {int(ping)}ms')


@bot.command()
async def sum(ctx, numOne: int, numTwo: int):
    '''
    If you're too lazy to do math then here you go
    '''
    await ctx.send(numOne + numTwo)


@bot.command()
async def roles(context):
    """Lists the current roles on the server."""

    roles = context.message.guild.roles
    result = "The roles on this server are: "
    for role in roles:
        result += role.name + ", "
    await context.send(result)


@bot.command()
async def group(ctx):
    '''
    Sends the group's link
    '''
    await ctx.send('https://www.roblox.com/groups/6268298/The-Drones-Army#!/about')


@bot.command()
async def info(ctx):
    '''
    Shows info about the server.
    '''
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Shows info about the server",
                          timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    await ctx.send(embed=embed)


@bot.command(aliases=['8ball'])
async def eightball(ctx, *, _ballInput: clean_content):
    """extra generic just the way you like it"""
    choiceType = random.choice(["(Affirmative)", "(Non-committal)", "(Negative)"])
    if choiceType == "(Affirmative)":
        prediction = random.choice(["It is certain ",
                                    "It is decidedly so ",
                                    "Without a doubt ",
                                    "Yes, definitely ",
                                    "You may rely on it ",
                                    "As I see it, yes ",
                                    "Most likely ",
                                    "Outlook good ",
                                    "Yes ",
                                    "Signs point to yes "]) + ":8ball:"
        emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0x3be801, description=prediction))
    elif choiceType == "(Non-committal)":
        prediction = random.choice(["Reply hazy try again ",
                                    "Ask again later ",
                                    "Better not tell you now ",
                                    "Cannot predict now ",
                                    "Concentrate and ask again "]) + ":8ball:"
        emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0xff6600, description=prediction))
    elif choiceType == "(Negative)":
        prediction = random.choice(["Don't count on it ",
                                    "My reply is no ",
                                    "My sources say no ",
                                    "Outlook not so good ",
                                    "Very doubtful "]) + ":8ball:"
        emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0xE80303, description=prediction))
    emb.set_author(name='Magic 8 ball',
                   icon_url='https://www.horoscope.com/images-US/games/game-magic-8-ball-no-text.png')
    await ctx.send(embed=emb)


@bot.command()
async def unoreverse(ctx):
    '''
    Uno reverse card. Credits to Davekuper2
    '''
    await ctx.send('https://tenor.com/view/reverse-card-uno-uno-cards-gif-13032597')

@bot.command()
async def accgen(ctx):
    '''
    Sends a link for some trusted account generators.
    '''
    await ctx.send('H-Gen: https://www.h-gen.xyz/ \n A-Gen: https://a-gen.xyz/ \n If you know more websites then make sure to suggest it')


bot.run(TOKEN)
