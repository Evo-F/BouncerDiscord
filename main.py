import json

import discord
import requests

from discord.ext import commands

import prompts

bot = commands.Bot(intents=discord.Intents.all(), command_prefix='$')


def register_commands():
    print("Attempting to register commands...")
    tokenfile = open("token.txt", "r")
    raw_token = tokenfile.read()
    url = "https://discord.com/api/v9/applications/854010619488894997/commands"
    headers = {
        "Authorization": "Bot %s" % bot_token
    }

    file = "commands/test.json"

    with open(file) as jsonfile:
        data = json.load(jsonfile)
        r = requests.post(url, headers=headers, json=data)
        print("Received Status Code: %d" % r.status_code)
        print(r.content)

    file = "commands/permissions_test.json"
    url = "https://discord.com/api/v9/applications/854010619488894997/guilds/854010059159634011/commands/permissions"
    with open(file) as jsonfile:
        data = json.load(jsonfile)
        r = requests.put(url, headers=headers, json=data)
        print("Received Status Code: %d" % r.status_code)


@bot.event
async def on_ready():
    # This event happens when the bot spins up.
    print('Logged on as {0}!'.format(bot.user))
    testprompt1 = prompts.NumberPrompt("What's your favorite number?")

    dict1 = vars(testprompt1)
    testprompt2 = prompts.prompt_from_dict(dict1)
    dict2 = vars(testprompt2)

    print("DICTIONARY OF RAW PROMPT")
    print(dict1)
    print("DICTIONARY OF RECONSTITUTED PROMPT")
    print(dict2)
    # bot.load_extension('commands')
    # register_commands()


# Sets the status of the bot, visible in user sidebar.
bot.activity = discord.Activity(name="Version 0.1", type=discord.ActivityType.competing)
# Starts the bot.
f = open("token.txt", "r")
bot_token = f.read()
bot.run(bot_token)

