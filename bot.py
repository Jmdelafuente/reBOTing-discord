# bot.py
import os

import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv
from random import choice
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

# client = discord.Client()
bot = Bot(command_prefix='!', description='Pequeño repollo cibernetico que quiere dar una mano.')
speakers = []

# Eventos
@bot.event
async def on_ready():
    # await bot.change_presence(activity = discord.Game('TERMINATOR'))
    await bot.change_presence(activity = discord.Activity(
                          type = discord.ActivityType.watching, 
                          name = 'PyDay Neuquén'))
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f"{bot.user} está conectado al siguiente guild:\n"
        f"{guild.name}(id: {guild.id})"
    )

@bot.event
async def on_message(message):
    if not message.author.bot:
        channels = ["general"]
        saludos = ["hola", 'Hola', 'HOLA', 'Buenas', 'buenas']
        saludo_bot = choice(saludos)
        if str(message.channel) in channels:  # Check if in correct channel
            if message.content in saludos:
                await message.channel.send(f"{saludo_bot} {message.author.mention}!")
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if (
            str(channel) == "general"
        ):  # We check to make sure we are sending the message in the general channel
            await channel.send_message(f"""Bienvenido al servidor {member.mention}!""")

# Comandos

@bot.command(name='users', help = 'Lista la cantidad de miembros')
async def cantidad_miembros(ctx):
    guild = discord.utils.get(bot.guilds, name=GUILD)
    await ctx.send(f"""# cantidad de Miembros: {guild.member_count}""")

@bot.command(name='pregunta', help = 'Envía una pregunta al speaker')
async def pregunta(ctx, *,pregunta=''):
    if pregunta == '':
        await ctx.send(f"{ctx.author.mention} no olvides escribir tu pregunta!")
    else:
        for user in speakers:
            if(user.dm_channel):
                dm = user.dm_channel
            else:
                dm = await user.create_dm()    
            await dm.send(f"{ctx.author.mention}: {pregunta}")

@bot.command(name='speaker', help="Darse de alta para recibir las preguntas")
async def alta_speaker(ctx):
    if(ctx.author.dm_channel):
        dm = ctx.author.dm_channel
    else:
        dm = await ctx.author.create_dm()
    if not ctx.author in speakers:
        speakers.append(ctx.author)
        await dm.send(f"Ahora vas a recibir las preguntas!")
    else:
        speakers.remove(ctx.author)
        await dm.send(f":cry: ya no recibis las preguntas")

bot.run(TOKEN)
