"""
house_bot.py

House M.D. is a discord.py bot designed to imitate the protagonist of the show House M.D. which ran from 2004 to 2012.
It uses the Chatterbot API to naturally respond to Discord messages. The bot is trained on all 175 episodes of the show
that aired across 8 seasons.
"""
import discord
from discord.ext import commands
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import asyncio
import json
import time
import random

# read config.json to get token and botid
config = open('config.json', 'r')
config = json.load(config)
botid = config['botid']
token = config['token']
prefix = config['prefix']

# initialise the chatterbot chatbot model
chatbot = ChatBot('House')
trainer = ListTrainer(chatbot)

# set command prefix
bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    print('Logged on as', bot.user)

@bot.event
async def on_message(message):
    # ignore self
    if message.author == bot.user:
            return
    # if bot is mentioned or dm'd
    if botid in message.content or message.guild is None:
            await respond(message)

    await bot.process_commands(message)

async def respond(message):
        time.sleep(random.randrange(0,4))
        message.content = message.content.replace(botid, '')
        response = chatbot.get_response(message.content)
        print(str(message.author) + ': ' + message.content)
        print(str(bot.user) + ': ' + str(response))
        #trainer.train([message.content, str(response)])
        async with message.channel.typing():
            time.sleep(round(len(str(response)) / 20, 0))
        await message.channel.send(response)

@bot.command(name='gethappy')
async def gethappy(ctx):
    # Gets voice channel of message author
    voice_channel = ctx.author.voice.channel
    channel = None
    if voice_channel != None:
        channel = voice_channel.name
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(source="gethappy.mp3")) # Sleep while audio is playing.

        while vc.is_playing(): # prevents the bot from disconnecting while it is playing
            #time.sleep(.1)
            await asyncio.sleep(1)

        await vc.disconnect()
    else:
        await ctx.send(str(ctx.author.name) + "is not in a channel.")
    # Delete command after the audio is done playing.
    await ctx.message.delete()

@bot.command(name="leave")
async def leave(ctx):
    if (ctx.voice_client.is_connected()):
        await ctx.voice_client.disconnect()

@bot.command(name="pause")
async def pause(ctx):
    ctx.voice_client.pause()

@bot.command(name="resume")
async def leave(ctx):
    ctx.voice_client.resume()

bot.run(token)
