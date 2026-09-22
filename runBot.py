# bot.py
import os
import discord
import json
import random
import linecache
import asyncio
from dotenv import load_dotenv

#load private things
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

#set discord intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

#initialize client
#initally built on discord.py, switched to py-cord
client = discord.Bot(intents=intents)

#when bot starts or on_ready is called
@client.event
async def on_ready():
    # Base channels
    client.admin = client.get_user(int(os.getenv("ADMIN_ID")))
    client.botId = client.get_user(int(os.getenv("BOT_ID")))
    client.gatorLog = client.get_channel(int(os.getenv("GATOR_LOG")))
    client.privateChannel = client.get_channel(int(os.getenv("PRIVATE")))
    client.receivingChannel = client.get_channel(int(os.getenv("RECEIVING")))

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

    #checks to see if the say command is locked or not
    with open('doingLoading.json', 'r') as file:
        client.sayLock = json.load(file)

    #all of these are if a station set or not..
    if (client.gatorLog is None):
        print("Log not set!")
        # if this doesn't load, doesn't matter much anyway.
    else:
        print("Log set!")
        successChannels.append("### SUCCESS: Log Set! ✅")
    #

    #
    if(client.admin is None):
        print("Admin not set!")
        await client.gatorLog.send("## FAIL: Admin Not Set ❌")
    else:
        print("Admin set!")
        successChannels.append("### SUCCESS: Admin Set! ✅")
    #

    #
    if(client.privateChannel is None):
        print("Private channel not set!")
        await client.gatorLog.send("## FAIL : Private Channel Not Set ❌")
    else:
        print("Private Channel Set!")
        successChannels.append("### SUCCESS: Private Channel Set! ✅")

    if(client.receivingChannel is None):
        print("Receiving Channel not set!")
        await client.gatorLog.send("## FAIL : Receiving Channel Not Set ❌")
    else:
        print("Receiving Channel Set!")
        successChannels.append("### SUCCESS: Receiving Channel Set! ✅")

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
            if x is None:
                client.channels.remove(x)

    isLoading = json.load(open("doingLoading.json"))

    #formats and sends message
    formattedMessage = '\n'.join(successChannels)
    newMessage = '# Loading is *Channels Set:*\n>>> {}'.format(formattedMessage)
    await client.gatorLog.send(f"{newMessage} \n# Loading is ```{isLoading}```")

    while(isLoading):
        #There are 86400 seconds in a day.
        #There are 259200 seconds in 3 days.
        #There are 3600 seconds in an hour.
        #There are 43200 in 12 hours.

        randomTime = random.randint(43200, 259200)
        randomTimeMinutes = int(randomTime/60)
        randomTimeHours = int(randomTimeMinutes/60)
        randomTimeDays = int(randomTimeHours/24)

        if randomTimeDays == 1:
            await client.gatorLog.send(f"Loading screen set for {randomTimeDays} day and {randomTimeDays % 24} hours from now.")
        elif randomTimeDays > 1:
            await client.gatorLog.send(f"Loading screen set for {randomTimeDays} days and {randomTimeDays % 24} hours from now.")
        elif randomTimeDays < 1:
            await client.gatorLog.send(f"Loading screen set for {randomTimeHours} hours and {randomTimeHours % 60} minutes from now.")

        await asyncio.sleep(randomTime)

        loadingTip = doloading()
        loadingTip = loadingTip.strip()
        loadingScreen = f"{loadingTip} <a:gatorLoading:1550230203777679511>"
        for x in client.channels:
            await x.send(loadingScreen)

@client.event
async def on_message(message):
    inReceivingChannels = False

    for x in client.channels:
        if message.channel == x:
            inReceivingChannels = True
        else:
            pass

    #Gay Stoned God is really coming in clutch huh,...
    if message.snapshots:
        if not isotheruser(message.author) and message.channel == client.privateChannel:
            if message.snapshots[0].message.content == "":
                sendMessage = "..."
            else:
                sendMessage = ""
            for x in client.channels:
                files = []
                stickers = []
                for a in message.snapshots[0].message.attachments:
                    files.append(await a.to_file())
                for a in message.snapshots[0].message.stickers:
                    stickers.append(await a.fetch())

                forwardedMessage = f"-# Forwarded..\n> {sendMessage}{message.snapshots[0].message.content}"

                await x.send(forwardedMessage, files=files, stickers=stickers)
    else:
        #Thanks to "gay stoned god" on the py-cord discord server for, over a year ago as i'm writing this, for figuring this out.
        if not isotheruser(message.author) and message.channel == client.privateChannel:
            for x in client.channels:
                files = []
                stickers = []
                for a in message.attachments:
                    files.append(await a.to_file())
                for a in message.stickers:
                    stickers.append(await a.fetch())

                await x.send(message.content, files=files, stickers=stickers)
        elif isotheruser(message.author) and inReceivingChannels:
            files = []
            stickers = []
            for a in message.attachments:
                files.append(await a.to_file())
            for a in message.stickers:
                stickers.append(await a.fetch())
            combinedFactors = f"### {message.author} from {message.guild} says... \n> __{message.content}__"
            await client.receivingChannel.send(combinedFactors, files=files, stickers=stickers)

@client.slash_command(name="reload", description="Reload the channels.")
async def reload(ctx: discord.ApplicationContext):
    if(ctx.author == client.admin):
        await ctx.respond("Reloaded!", ephemeral=True)
        await on_ready()
    else:
        await ctx.respond("Please contact InvaderGator to reload channels.", ephemeral=True)

@client.slash_command(name="github", description="View code.")
async def github(ctx: discord.ApplicationContext):
    ctx.respond("https://github.com/InvaderGator/Gator-Messager", ephemeral=True)

@client.slash_command(name="toggle_loading", description="Toggle loading.")
async def toggle_loading(ctx: discord.ApplicationContext):
    isTrue = json.load(open("doingLoading.json"))
    change = not isTrue

    json.dump(change, open("doingLoading.json", "w"))
    await ctx.respond(f"## Loading screens are now {change}.", ephemeral=True)
    await on_ready()

def isotheruser(user):
    if user == client.admin:
        return False
    elif user == client.botId:
        return False
    else:
        return True

def doloading():
    randomNum = random.randint(1, 1000)
    randomTip = linecache.getline("loadingScreens.txt", randomNum)
    return randomTip

client.run(TOKEN)
