# bot.py
import os
from ftplib import print_line

import discord
from dotenv import load_dotenv

from discord.ext import commands
#
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    client.admin = client.get_user(int(os.getenv("ADMIN_ID")))

    client.gatorLog = client.get_channel(int(os.getenv("GATOR_LOG")))

    client.channels = []

    client.gatorTesting = client.get_channel(int(os.getenv("GATOR_TESTING1")))
    client.channels.append(client.gatorTesting)

    client.gatorTesting2 = client.get_channel(int(os.getenv("GATOR_TESTING2")))
    client.channels.append(client.gatorTesting2)

    client.a1Bottle = client.get_channel(int(os.getenv("A1_BOTTLE")))
    client.channels.append(client.a1Bottle)

    client.fags = client.get_channel(int(os.getenv("FAGS")))
    client.channels.append(client.fags)

    #
    if (client.gatorLog == None):
        print("Log not set!")
    else:
        print("Log set!")
        await client.gatorLog.send(" ### SUCCESS: Log Set! ✅")
    #

    #
    if(client.admin == None):
        print("Admin not set!")
        await client.gatorLog.send("## FAIL: Admin Not Set ❌")
    else:
        print("Admin set!")
        await client.gatorLog.send("### SUCESS: Admin Set! ✅")
    #

    counter = 0
    for x in client.channels:
        xStr = str(x)

        if(x == None):
            counter += 1
        else:
            print(xStr + " set!")
            await client.gatorLog.send("### Success: " + xStr + " Set! ✅")

    if(counter != 0):
        counterStr = str(counter)
        print("FAIL: Channels not set: " + counterStr + " ❌")
        await client.gatorLog.send("FAIL: Channels not set: " + counterStr + " ❌")

        channelsStr = []
        for x in client.channels:
            channelsStr.append(str(x))
        print(list(enumerate(channelsStr)))
        await client.gatorLog.send(list(enumerate(channelsStr)))

        for x in client.channels:
            if x == None:
                client.channels.remove(x)

@client.event
async def on_message(message):
    messageAuthor = str(message.author)

    for x in client.channels:
        if message.author == client.admin and isinstance(message.channel, discord.DMChannel):
            if message.attachments:
                for y in message.attachments:
                    messageImage = y.url
                    await x.send(messageImage)
                    if (message.content != ""):
                        await x.send(message.content)
            else:
                await x.send(message.content)

client.run(TOKEN)