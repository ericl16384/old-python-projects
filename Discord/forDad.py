TOKEN = "YOUR TOKEN HERE"


import logging, time
import discord


def messageToStr(message):
    out = ""

    # Is it TextChannel or DMChannel?
    if isinstance(message.channel, discord.TextChannel):
        out += message.author.guild.name+": "+message.channel.name+": "
    elif isinstance(message.channel, discord.DMChannel):
        out += "DIRECT: "
    elif isinstance(message.channel, discord.GroupChannel):
        raise NotImplementedError

    # Their name
    out += message.author.name+"#"+message.author.discriminator

    # Is it Member or User?
    if isinstance(message.author, discord.Member):
        if not message.author.nick == None:
            out += "\""+message.author.nick+"\""
    elif isinstance(message.author, discord.User):
        pass
    else:
        raise NotImplementedError
    
    # Add the content and return
    out += ": "+message.content
    return out


logger = logging.getLogger("discord")
logger.setLevel(logging.INFO) # Do not allow DEBUG messages through
handler = logging.FileHandler(filename="bot.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("{asctime}: {levelname}: {name}: {message}", style="{"))
logger.addHandler(handler)

logger.info("Starting up the client")


client = discord.Client()

@client.event
async def on_error(event, *args, **kwargs):
    logger.exception(f"{event} error:\nargs: {args},\nkwargs: {kwargs}")

    t = time.localtime()
    print(f"ERROR at {t[0]}-{t[1]}-{t[2]} {t[3]}:{t[4]}:{t[5]}")

@client.event
async def on_ready():
    print(f"Reconnected as {client.user}")

@client.event
async def on_message(message):
    # Log message
    logger.info(messageToStr(message))

    # Ignore messages from self
    if message.author == client.user:
        return

    # Ignore caps
    if "!hello" in message.content.lower():
        await message.channel.send(f"Hello, {message.author.mention}!")

client.run(TOKEN)
