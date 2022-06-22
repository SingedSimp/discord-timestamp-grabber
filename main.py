import json # Used to create JSON output
# Pycord Stuff
import discord 
from discord.ext import commands
# Enviromental Variable stuff
from os import environ
from dotenv import load_dotenv

# Load API Key
# Place api key in a .env file as: "API=<instert api key here>"
load_dotenv()
key = environ["API"]
# Setup discord bot permissions
intents = discord.Intents.default()
intents.message_content = True
# Set command prefix and intentions
bot = commands.Bot(command_prefix=">", intents=intents)

# Used to parse the written timestamps into json
# Also an abomination
def parseSchedule(schedule):
    while "" in schedule: # Remove all empty lines
        schedule.remove("")
    fsched = []
    tarr = []
    count = 1
    for line in schedule:
        if count == 1:
            tarr.append(line)
        elif count == 2:
            tarr.append(line)
            count = 0
            tdict = {
                "name": tarr[0],
                "time": tarr[1].split(":")[1]
            }
            fsched.append(tdict)
            tarr.pop(0)
            tarr.pop(0)
        count+=1
    return fsched

# Bot command to grab messages, seperate for debugging purposes
@bot.command()
async def grab(ctx):
    latest = None
    channel = await commands.TextChannelConverter().convert(ctx, argument="986080013789065289")
    async for message in channel.history(limit=200):
        if "#0000" in str(message.author): # Webhook users start with #0000
            if "<t" in message.content and ">" in message.content:
                latest = message.content
                break
    return latest
# Bot command to print the formatted timestamps into "s.txt" 
@bot.command()
async def prin(ctx):
    sch = await grab(ctx)
    sch = sch.replace("*", "") # Issues with strip
    schedule = sch.split("\n")
    schedule = parseSchedule(schedule)
    tdict = {}
    counter = 1
    for s in schedule:
        tdict[f"Time {counter}"] = s # Generic names, starting at 1
        counter += 1
    json_v = json.dumps(tdict, indent = 4)
    with open("out.txt", "w+") as f:
        f.write(json_v.replace("[", "{").replace("]", "}"))
        


        
bot.run(str(key)) # Start bot