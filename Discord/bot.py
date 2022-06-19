# https://discord.com/api/oauth2/authorize?client_id=768264709258084384&permissions=67176449&scope=bot
TOKEN = "NzY4MjY0NzA5MjU4MDg0Mzg0.X498RA.jMBlHN511Fzqpczui2h6X4t_D4U" # Very secret!


# Imports

import logging, time
import discord, discordUtil


# Debug

if False: # Set to False normally
    discordUtil.logger.setLevel(logging.DEBUG)


# Functions

def raiseException():
    raise Exception("Caused by the causeError command")

def makeCharacter(): # Generator
    msg = yield {"message": "What is your character's name?"}
    name = msg.content

    msg = yield {"message": "Do you want to save your character before playing?"}
    while True:
        if msg.content.startswith("y"):
            yield {"message": f"Character \"{name}\" saved!"}
            break

        elif msg.content.startswith("n"):
            break

        else:
            yield {"message": "y/n"}
    
    # Call play()
    raise NotImplementedError


# Setup

discordUtil.logger.info("Starting up the client")

client = discord.Client()

cmd = discordUtil.CommandHandler(client)

def showAllCommands():
    return cmd.strCommands(forceAll=True)

cmd.addCommands({
    # Regular
    "mystery": {
        "data": {"message": "TOP SNEAKY\n"*10},
        "desc": "..."
    },

    # No prefix
    "hello": {
        "data": {"message": "Hello!"},
        "desc": "Exchange a friendly greeting",
        "alternatePrefix": "",
        "matchCase": False
    },
    "bye": {
        "data": {"message": "Goodbye!"},
        "desc": "Say a solemn farewell",
        "alternatePrefix": "",
        "matchCase": False
    },

    # Unlisted
    "hi": {
        "data": {"message": "Hello!"},
        "unlisted": True,
        "alternatePrefix": "",
        "matchCase": False,
        "desc": "alternate form of hello"
    },
    "brb": {
        "data": {"message": "See you later!"},
        "unlisted": True,
        "alternatePrefix": "",
        "matchCase": False,
        "desc": "nice hidden thing"
    },
    "hannah": {
        "data": {"message": "You may dispense the verbal thwackage, <@!333138212107190274>."},
        "findMode": "search",
        "alternatePrefix": "",
        "unlisted": True,
        "matchCase": False,
        "desc": "Per request by <@!333138212107190274>."
    },
    "tada": {
        "data": {"message": ":)"},
        "unlisted": True,
        "alternatePrefix": "",
        "findMode": "search",
        "matchCase": False,
        "desc": "for when things are great"
    },

    # Testing (unlisted)
    "displayCommands": {
        "data": {"message": {"function": showAllCommands}},
        "unlisted": True,
        "desc": "DO NOT USE IN A PUBLIC SPACE",
        "findMode": "exact",
        "alternatePrefix": "!!"
    },
    "causeError": {
        "data": {"function": raiseException},
        "unlisted": True,
        "desc": "for debugging messages",
        "findMode": "exact",
        "alternatePrefix": "!!"
    },
    "play": {
        "data": {"getIterator": makeCharacter},
        "unlisted": True,
        "desc": "Not ready"
    }
})


# Events MOVE TO discordUtil

@client.event
async def on_error(event, *args, **kwargs):
    discordUtil.logger.exception(f"{event} error:\nargs: {args}\nkwargs: {kwargs}")

    t = time.localtime()
    print(f"ERROR at {t[0]}-{t[1]}-{t[2]} {t[3]}:{t[4]}:{t[5]}")

@client.event
async def on_ready():
    print(f"Reconnected as {client.user}")

@client.event
async def on_message(message):
    data = cmd.run(message)

    if isinstance(data, dict):
        if "message" in data.keys():
            await message.channel.send(data["message"])
        
        # Other features that rely on Discord

#@client.event
#async def on_message_delete(message):
#    discordUtil.logger.info(f"deleted message: {message}")

# Causes error
#@client.event
#async def on_message_edit(before, after):
#    discordUtil.logger.info(f"edited message: {discordUtil.messageToStr(before)}\nnew message: {discordUtil.messageToStr(after)}")


# Run

client.run(TOKEN)
