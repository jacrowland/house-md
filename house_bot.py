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
import os
import youtube_dl

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

"""
Music Bot Functionality
"""
servers = {}

async def getYoutubeVideoInfo(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloadedsongs/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        song_info = ydl.extract_info(url, download=False)
    # actual song url is song_info["formats"][0]["url"]
    return song_info

async def downloadYoutubeVideo(url, ctx):
    outputPath = 'songs/' + str(ctx.guild.id) + '/' + '%(title)s.%(ext)s'
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': outputPath,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        video = ydl.download([url])

@bot.command(name='play')
async def play(ctx):
    print(ctx.author.voice)
    if not ctx.author.voice == None:
        voice_channel = ctx.author.voice.channel
        channel = None
        if voice_channel != None:
            channel = voice_channel.name

        if ctx.guild.id not in servers:
            servers[ctx.guild.id] = {'queue': []}
        server = servers[ctx.guild.id]

        args = str(ctx.message.content).split(" ")
        if len(args) > 0:
            server['queue'].append(args[1])
            video_info = await getYoutubeVideoInfo(args[1])
            await ctx.send(video_info['title'] + " added to queue.")

        print(server['queue'])
        await ctx.message.delete()

        try:
            vc = await voice_channel.connect()
        except:
            return

        if not vc.is_playing():
            while len(server['queue']) != 0:
                url = server['queue'].pop()
                video = await downloadYoutubeVideo(url, ctx)
                video_info = await getYoutubeVideoInfo(url)
                path = 'songs\\' + str(ctx.guild.id) + '\\' + video_info['title'] +'.mp3'
                vc.play(discord.FFmpegPCMAudio(source=path))
                # prevents the bot from disconnecting while it is playing
                while vc.is_playing():
                    #time.sleep(.1)
                    await asyncio.sleep(1)
                os.remove(path) # delete downloaded audio after playback
            await vc.disconnect()

@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client.is_connected() or ctx.voice_client.is_playing():
        await ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

@bot.command(name="pause")
async def pause(ctx):
    ctx.voice_client.pause()

@bot.command(name="resume")
async def leave(ctx):
    ctx.voice_client.resume()




bot.run(token)

"""
@bot.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['pl'])
async def play(ctx, url:str):
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id), before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5')
    players[server.id] = player
    player.start()
"""
