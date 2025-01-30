# bot.py
import os
import random
import re

import discord
from dotenv import load_dotenv
from datetime import date

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
KEK_BDAYS_NAME=["Paul", "Adrian", "Ngadhnim", "Bibi", "Jasmin", "Robin", "Thomas", "Marvin", "Andre"]
KEK_BDAYS_DATE=["01-25", "04-19", "08-01", "01-30", "06-27", "12-07", "08-21", "07-31", "02-03"]
CHANNELS = [1331704562779689091, 1161705210280955986]

intentsB = discord.Intents.default()
intentsB.members = True
intentsB.message_content = True

today = str(date.today())
print(f'today: {today} \n')   # raw date

trimmed_today = today[5:]
print(f'trimmed_today: {trimmed_today} \n')

client = discord.Client(intents = intentsB)

@client.event
async def on_ready():

    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is now online on: \n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    print(f'is now checking for bdays... \n')

    is_BDAY = False
    x = 0
    for String in KEK_BDAYS_NAME:
        print(f'Kek: {String}, Bday: {KEK_BDAYS_DATE[x]}')
        if(KEK_BDAYS_DATE[x] == trimmed_today):
            is_BDAY = True
            who = x
        x = x + 1

    print(f'is_BDAY: {is_BDAY}')
    if(is_BDAY):
        channel = client.get_channel(1331704562779689091) #  Gets channel from internal cache
        at_all = '@everyone '
        kek_name = KEK_BDAYS_NAME[who]
        start_message = 'Heute hat jemand Geburtstag! '
        end_message = ', alles gute zum Geburtstag!'
        starter_message = at_all + start_message + kek_name + end_message
        await channel.send(starter_message) #  Sends message to channel



@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to this server!'
    )

@client.event
async def on_message(message):
    if message.channel.id in CHANNELS:
        if message.author == client.user:
            return

        brooklyn_99_quotes = [
            'I\'m the human form of the 💯 emoji.',
            'Bingpot!',
            (
                'Cool. Cool cool cool cool cool cool cool, '
                'no doubt no doubt no doubt no doubt.'
            ),
        ]

        if message.content == '99!':
            response = random.choice(brooklyn_99_quotes)
            await message.channel.send(response)
        elif message.content == 'raise-exception':
            raise discord.DiscordException
        elif re.search('kek',message.content):
            response = 'kek'
            await message.channel.send(response)
        
        
@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


client.run(TOKEN)