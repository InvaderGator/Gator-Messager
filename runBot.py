# bot.py
import os
import discord
import json
from dotenv import load_dotenv

from discord.ext import commands
#
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
#intents.messages = True
intents.members = True

client = discord.Bot(intents=intents)

@client.event
async def on_ready():
    client.admin = client.get_user(int(os.getenv("ADMIN_ID")))

    client.gatorLog = client.get_channel(int(os.getenv("GATOR_LOG")))

    client.privateChannel = client.get_channel(int(os.getenv("PRIVATE")))

    client.channels = []

    client.gatorTesting = client.get_channel(int(os.getenv("GATOR_TESTING1")))
    client.channels.append(client.gatorTesting)

    client.gatorTesting2 = client.get_channel(int(os.getenv("GATOR_TESTING2")))
    client.channels.append(client.gatorTesting2)

    client.a1Bottle = client.get_channel(int(os.getenv("A1_BOTTLE")))
    client.channels.append(client.a1Bottle)

    client.fags = client.get_channel(int(os.getenv("FAGS")))
    client.channels.append(client.fags)

    channels = []

    with open('banlist.json', 'r') as file:
        client.bannedUsers = json.load(file)

    bannedUserNames = []
    for x in client.bannedUsers:
        bannedUserNames.append(client.get_user(x).name)

    formattedBanList = "\n".join(bannedUserNames)
    banListMessage = '# *Users Banned:*\n>>> {}'.format(formattedBanList)
    await client.gatorLog.send(banListMessage)
    print("BANNED USERS:" + str(client.bannedUsers))

    #
    if (client.gatorLog == None):
        print("Log not set!")
        # if this doesn't load, doesn't matter much anyway.
    else:
        print("Log set!")
        channels.append("### SUCCESS: Log Set! ✅")
    #

    #
    if(client.admin == None):
        print("Admin not set!")
        await client.gatorLog.send("## FAIL: Admin Not Set ❌")
    else:
        print("Admin set!")
        channels.append("### SUCCESS: Admin Set! ✅")
    #

    counter = 0
    for x in client.channels:
        xStr = str(x)

        if(x == None):
            counter += 1
        else:
            print(xStr + " set!")
            channels.append("### SUCCESS: " + xStr + " Set! ✅")

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

    formattedMessage = '\n'.join(channels)
    newMessage = '# *Channels Set:*\n>>> {}'.format(formattedMessage)
    await client.gatorLog.send(newMessage)

@client.event
async def on_message(message):
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
    if not message.author == client.admin and isinstance(message.channel, discord.DMChannel):
        if message.attachments:
            for y in message.attachments:
                messageImage = y.url
                await client.privateChannel.send("*" + message.author.name + "*" + "SENT" + messageImage)
                if (message.content != ""):
                    await client.privateChannel.send("*" + message.author.name + " says...* " "'" + "**" + message.content + "**")
        else:
            await client.privateChannel.send("*" + message.author.name + " says...* " "'" + "**" + message.content + "**")
        print(message.author.name + " says... " + "'" + message.content + "'")

@client.slash_command(name="reload", description="Reload the channels.")
async def reload(ctx: discord.ApplicationContext):
    if(ctx.author == client.admin):
        await ctx.respond("Reloaded!")
        await on_ready()
    else:
        await ctx.respond("Please contact InvaderGator to reload channels.")

@client.slash_command(name="say", description="Say something to the bot!", ephemeral = True)
async def say(ctx: discord.ApplicationContext, message: str):
    banned = False
    userID = ctx.author.id
    for x in client.bannedUsers:
        int1 = int(x)
        int2 = int(userID)

        if(int1 == int2):
            banned = True

    if not banned:
        for x in client.channels:
            await x.send("*" + ctx.author.name + "*: " + message)
        await ctx.respond("Message sent.")
    else:
        await ctx.respond("Ur banned, loser.")

@client.slash_command(name="adminban", description="DEATH.")
async def adminban(ctx: discord.ApplicationContext, message: str):
    newMessageArray = []

    for x in message:
        if(not(x == "<" or x == ">" or x == "@")):
            newMessageArray.append(x)

    newMessage = "".join(newMessageArray)
    user = client.get_user(int(newMessage))

    if(ctx.author == client.admin):
        client.bannedUsers.append(int(newMessage))
        json.dump(client.bannedUsers, open("banlist.json", "w"))
        await ctx.respond("User, " + user.mention + " banned from saybot command!")
        await user.send("You have been banned from gator messenger! Please contact @invadergator to get unbanned.")
        await on_ready()

@client.slash_command(name="adminunban", description="life. (:")
async def adminunban(ctx: discord.ApplicationContext, message: str):
    newMessageArray = []
    newMessage = ""

    for x in message:
        if(not(x == "<" or x == ">" or x == "@")):
            newMessageArray.append(x)

    newMessage = "".join(newMessageArray)
    user = client.get_user(int(newMessage))

    if(ctx.author == client.admin):
        newMessageArray = []
        for x in client.bannedUsers:

            int1 = int(x)
            int2 = int(newMessage)
            print(x)
            print(newMessage)

            if(int1 != int2):
                print("TRIGGER")
                newMessageArray.append(x)
        client.bannedUsers = newMessageArray

        json.dump(client.bannedUsers, open("banlist.json", "w"))
        await ctx.respond("User, " + user.mention + " unbanned from saybot command!")
        await on_ready()

client.run(TOKEN)