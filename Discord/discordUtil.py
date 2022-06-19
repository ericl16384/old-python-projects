"""Discord API utility made by Eric Lewis.

Started work 10/20/2020

Makes Discord bots easier and faster to write, via automatic command handling."""


# TODO #
# allow generator commands --------- allow CommandHandler commands???
# make command output a special object
# allow changing base config
# allow ignoreBot (default to True)
# change alternatePrefix to prefix
# Automate the client functions


# Setup

import logging
import discord

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO) # Do not allow DEBUG messages through
handler = logging.FileHandler(filename="bot.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("{asctime}: {levelname}: {name}: {message}", style="{"))
logger.addHandler(handler)


# Functions

def messageToStr(message):
    # Init string
    out = ""

    # From
    if isinstance(message.channel, discord.TextChannel):
        out += message.author.guild.name+": "+message.channel.name+": "
    elif isinstance(message.channel, discord.DMChannel):
        out += "DIRECT: "
    elif isinstance(message.channel, discord.GroupChannel):
        raise NotImplementedError

    # Name
    out += message.author.name+"#"+message.author.discriminator

    # Nickname
    if isinstance(message.author, discord.Member):
        if not message.author.nick == None:
            out += "\""+message.author.nick+"\""
    elif isinstance(message.author, discord.User):
        pass
    elif isinstance(message.author, discord.ClientUser):
        pass
    else:
        raise NotImplementedError
    
    # Add the content and return
    out += ": "+message.content
    return out


# Main

class CommandHandler:
    def __init__(self, client, prefix="!"):
        self.client = client
        self.prefix = prefix

        self.cmds = {}
        self.addCommands({
            "help": {
                "data": {"message": {"function": self.strCommands}},
                "desc": "Displays a list of all commands"
            }
        })

        self.iteratorSessions = {}
    
    def addCommands(self, cmds):
        """Overwrites commands with keys in the input dict"""
        for i in cmds.keys():
            # Default
            if isinstance(cmds[i], dict):
                self.cmds[i] = cmds[i]

            # String shorthand for messages
            #elif isinstance(cmds[i], str):
            #    self.cmds[i] = {"data": {"message": cmds[i]}}
            
            # WRONG
            else:
                raise TypeError
            

            # Flush out the command
            if not "data" in self.cmds[i].keys():
                raise ValueError("Commands must have a data field.")
            if not "desc" in self.cmds[i].keys():
                self.cmds[i]["desc"] = ""
            if not "findMode" in self.cmds[i].keys():
                self.cmds[i]["findMode"] = "start"
            if not "matchCase" in self.cmds[i].keys():
                self.cmds[i]["matchCase"] = True
            if not "alternatePrefix" in self.cmds[i].keys():
                self.cmds[i]["alternatePrefix"] = False
            if not "unlisted" in self.cmds[i].keys():
                self.cmds[i]["unlisted"] = False

    def getCommands(self):
        return self.cmds
    
    def strCommands(self, forceAll=False):
        # Constants
        sep = f"\n    "

        # Setup
        cmds = self.getCommands()
        maxCmdLen = 0
        maxPreLen = len(self.prefix)
        for i in cmds.keys():
            maxCmdLen = max(maxCmdLen, len(i))
            if not cmds[i]["alternatePrefix"] == False:
                maxPreLen = max(maxPreLen, len(cmds[i]["alternatePrefix"]))
        maxCmdLen += 1

        # Create and return the output message
        out = "```txt\nCommands:"
        for i in cmds.keys():
            # If unlisted and not force
            if cmds[i]["unlisted"] and not forceAll:
                continue

            if cmds[i]["alternatePrefix"] == False:
                prefix = self.prefix
            else:
                prefix = cmds[i]["alternatePrefix"]

            out += sep+(maxPreLen-len(prefix))*" "+prefix+i+(maxCmdLen-len(i))*" "

            # If unlisted (and inherently force)
            if cmds[i]["unlisted"]:
                out += "(UNLISTED) "
            
            out += cmds[i]["desc"]
        return out + "\n```"

    
    def isIteratorSession(self, message, id=None):
        if not id:
            id = message.author.id

        return id in self.iteratorSessions.keys()

    def addIteratorSession(self, id, getIterator):
        if self.isIteratorSession(None, id):
            # They are already in an iterator
            raise KeyError

        else:
            # Get iterator, and advance it to the first yield
            self.iteratorSessions[id] = getIterator()
            self.iteratorSessions[id].send(None)
        
    def removeIteratorSession(self, id):
        if id in self.iteratorSessions.keys():
            self.iteratorSessions.pop(id)
            
        else:
            # They are not in an iterator
            raise KeyError
    
    def continueIteratorSession(self, message, id=None):
        if not id:
            id = message.author.id

        try:
            # Return the next item in the iterator
            return self.iteratorSessions[id].send(message)
        except StopIteration:
            self.removeIteratorSession(id)
            return False


    # Move out of class
    def logMessage(self, message):
        logger.debug(message)
        logger.info(messageToStr(message))

    def doDataLogic(self, data, message, ignoreError=False):
        # Standard format
        if isinstance(data, dict):
            toPop = []
            for i in data.keys():
                # Recurse
                data[i] == self.doDataLogic(data[i], message, ignoreError=True)

                # Message
                if i == "message":
                    # Regular
                    if isinstance(data[i], str):
                        if len(data[i]) == 0:
                            raise ValueError("message argument must not be len 0\n"+str(data)+"\n\""+message.content+"\"")

                    # Convert the contents into a string separated by \n

                    elif isinstance(data[i], list):
                        if len(data[i]) == 0:
                            #logger.warning("doDataLogic: message got a len 0 list: "+str(data))
                            raise ValueError("message argument must not be len 0\n"+str(data)+"\n\""+message.content+"\"")

                        data[i] = "\n".join(data[i])

                    elif isinstance(data[i], dict):
                        # Turn dict into str

                        if len(data[i]) == 0:
                            #toPop.append(i)
                            #logger.warning("doDataLogic: message got a len 0 dict: "+str(data))
                            raise ValueError("message argument must not be len 0\n"+str(data)+"\n\""+message.content+"\"")

                        elif len(data[i]) == 1:
                            # Bad solution, but it works
                            for j in data[i].keys():
                                data[i] = data[i][j]

                        else:
                            newMessage = ""
                            for j in data[i].keys():
                                newMessage += j+": "+data[i][j]+"\n"
                            data[i] == newMessage

                # Function
                elif i == "function":
                    # Run the function and remove it if it returns None
                    data[i] = data[i]()
                    if data[i] == None:
                        toPop.append(i)
                
                # Iterator
                elif i == "getIterator":
                    # Hand them over to the iterator
                    self.addIteratorSession(message.author.id, data[i])
                    toPop.append(i)
                    return self.continueIteratorSession(message)

                
                # Other features that edit this object


                else:
                    raise NotImplementedError

            # Pop extraneous items (cannot do while iterating through keys)
            for i in toPop:
                data.pop(i)
        
        # Bad type!
        else:
            if not ignoreError:
                raise TypeError(type(data))
        
        # Return
        return data

    def run(self, message):
        # Log
        self.logMessage(message)

        # Quit if sent by this bot
        if message.author == self.client.user:
            return

        # If they are in an iterator, hand them over to the iterator
        if self.isIteratorSession(message):
            ans = self.continueIteratorSession(message)

            logger.info("Answer is: "+str(ans))

            if not ans == False:
                return ans # Do not send through doDataLogic, as this handled by the iterator


        # Look for commands
        cmds = self.getCommands()
        for i in cmds.keys():
            # Formulate cmd
            if cmds[i]["alternatePrefix"] == False:
                cmd = self.prefix + i
            else:
                cmd = cmds[i]["alternatePrefix"] + i
            
            # Formulate msg
            if cmds[i]["matchCase"]:
                msg = message.content
            else:
                msg = message.content.lower()


            # matchCase
            if not cmds[i]["matchCase"]:
                cmd = cmd.lower()
                msg = msg.lower()


            # Looking for cmd in msg

            if cmds[i]["findMode"] == "exact":
                # Equals!
                if msg == cmd:
                    return self.doDataLogic(cmds[i]["data"], message=message)

            elif cmds[i]["findMode"] == "start":
                # Startswith!
                if msg.startswith(cmd):
                    return self.doDataLogic(cmds[i]["data"], message=message)
            
            elif cmds[i]["findMode"] == "end":
                # Endswith!
                if msg.endswith(cmd):
                    return self.doDataLogic(cmds[i]["data"], message=message)
            
            elif cmds[i]["findMode"] == "search":
                # In!
                if cmd in msg:
                    return self.doDataLogic(cmds[i]["data"], message=message)

            # Bad parameter
            else:
                raise ValueError
