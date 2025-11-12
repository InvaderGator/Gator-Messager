# bot.py
import os
import discord
import json
from dotenv import load_dotenv

#load private things
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

#set discord intents
intents = discord.Intents.default()
intents.members = True

#initialize client
#initally built on discord.py, switched to py-cord
client = discord.Bot(intents=intents)

#when bot starts or on_ready is called
@client.event
async def on_ready():
    # Base channels
    client.admin = client.get_user(int(os.getenv("ADMIN_ID")))
    client.gatorLog = client.get_channel(int(os.getenv("GATOR_LOG")))
    client.privateChannel = client.get_channel(int(os.getenv("PRIVATE")))

    #channels that are stored in env
    #different from successChannels
    client.channels = []

    client.gatorTesting = client.get_channel(int(os.getenv("GATOR_TESTING1")))
    client.channels.append(client.gatorTesting)

    client.gatorTesting2 = client.get_channel(int(os.getenv("GATOR_TESTING2")))
    client.channels.append(client.gatorTesting2)

    client.a1Bottle = client.get_channel(int(os.getenv("A1_BOTTLE")))
    client.channels.append(client.a1Bottle)

    client.fags = client.get_channel(int(os.getenv("FAGS")))
    client.channels.append(client.fags)

    #for print statements and if logic
    successChannels = []

    #opens banlist
    with open('banlist.json', 'r') as file:
        client.bannedUsers = json.load(file)

    #gets array of banned users
    bannedUserNames = []
    for x in client.bannedUsers:
        #gets names of banned users for printing
        bannedUserNames.append(client.get_user(x).name)

    #formats and sends banned user messages in gatorLog
    formattedBanList = "\n".join(bannedUserNames)
    banListMessage = '# *Users Banned:*\n>>> {}'.format(formattedBanList)
    await client.gatorLog.send(banListMessage)
    print("BANNED USERS:" + str(client.bannedUsers))


    #all of these are if a station set or not.
    #
    if (client.gatorLog == None):
        print("Log not set!")
        # if this doesn't load, doesn't matter much anyway.
    else:
        print("Log set!")
        successChannels.append("### SUCCESS: Log Set! ✅")
    #

    #
    if(client.admin == None):
        print("Admin not set!")
        await client.gatorLog.send("## FAIL: Admin Not Set ❌")
    else:
        print("Admin set!")
        successChannels.append("### SUCCESS: Admin Set! ✅")
    #

    #counter is for seeing if there are channels not set, and if there are, then how many channels aren't set
    counter = 0
    for x in client.channels:
        #needs to be string
        #easier to do variable
        xStr = str(x)

        if(x == None):
            counter += 1
        else:
            print(xStr + " set!")
            successChannels.append("### SUCCESS: " + xStr + " Set! ✅")

    #if counter is not 0, then print which channels are set, so you can use process of elimination to figure out which did not.
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

    #formats and sends message
    formattedMessage = '\n'.join(successChannels)
    newMessage = '# *Channels Set:*\n>>> {}'.format(formattedMessage)
    await client.gatorLog.send(newMessage)

#i must dm the bot to send messages to channels
#for private dms, gets rerouted to private channel.
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

    banned = False
    userID = message.author.id
    for x in client.bannedUsers:
        int1 = int(x)
        int2 = int(userID)

        if(int1 == int2):
            banned = True

    if not message.author == client.admin and not banned and isinstance(message.channel, discord.DMChannel):
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

@client.slash_command(name="say", description="Say something to the bot!")
async def say(ctx: discord.ApplicationContext, message: str):
    banned = False
    userID = ctx.author.id
    for x in client.bannedUsers:
        int1 = int(x)
        int2 = int(userID)

        if(int1 == int2):
            banned = True

    if not banned and client.sayLock != True:
        for x in client.channels:
            await x.send("-# *" + ctx.author.name + "*: " + message)
        await ctx.respond("Message sent.", ephemeral=True)
    else:
        await ctx.respond("Ur banned, loser.", ephemeral=True)

@client.slash_command(name="adminlock", description="locks say command.")
async def adminlock(ctx: discord.ApplicationContext):
    if(ctx.author == client.admin):
        client.sayLock = True
        await ctx.respond("Say command locked.")

@client.slash_command(name="adminunlock", description="unlocks say command.")
async def adminunlock(ctx: discord.ApplicationContext):
    if(ctx.author == client.admin):
        client.sayLock = True
        await ctx.respond("Say command unlocked.")

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
        await user.send("User, " + user.name  + ", have been banned from gator messenger! Please contact @invadergator to get unbanned.")
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