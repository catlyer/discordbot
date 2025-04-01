import discord
from discord.ext import commands
import os
import yt_dlp
from pytubefix import Search
from config import DISCORD_BOT_TOKEN

import nest_asyncio
nest_asyncio.apply()

intents = discord.Intents.all()
prefix = "n!"
bot = commands.Bot(command_prefix=prefix,intents=intents)

ytdl_format = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": False,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "default_search": "auto",
    "source_address": "0.0.0.0",}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def join(ctx):
    '''
    Used to make the bot join VC
    '''
    if not ctx.author.voice:
        await ctx.send("You are not connected to a voice channel.")
        return
    channel = ctx.author.voice.channel
    try:
        print("attempting to join vc")
        await ctx.author.voice.channel.connect()
        print("connecting to vc")
        await ctx.send(f"Joined {channel.name}")
        print("connected to vc")
    except discord.ClientException as e:
        await ctx.send(f"Failed to join voice channel: {e}")

@bot.command()
async def leave(ctx):
    '''
    Used to make the bot leave a VC
    '''
    await ctx.voice_client.disconnect()

@bot.command()
async def ping(ctx):
    '''
    Used to test the latency of the bot
    '''
    latency = bot.latency
    await ctx.send(latency)

@bot.command()
async def linkplay(ctx, video_url):
    '''
    Plays a YouTube video in the voice channel.
    Usage: n!linkplay [Url to youtube video]
    '''
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()
    try:
        with yt_dlp.YoutubeDL(ytdl_format) as ydl:
            info = ydl.extract_info(video_url, download=False)
            filename = ydl.prepare_filename(info)
            await ctx.send("Downloading... This might take a while depending on the video length")
            ydl.download([video_url])
    except Exception as e:
        await ctx.send(f"An error occurred: (Downloading phase): {e}")
        return
    try:
        source = discord.FFmpegOpusAudio(executable="ffmpeg", source=filename)
        source.read()
        ctx.voice_client.play(source)
        await ctx.send(f"Currently playing: [{info['title']}]"+f"(<{video_url}>)")
        os.remove(filename)
    except Exception as e:
        await ctx.send(f"An error occurred: (Playing phase): {e}")

@bot.command()
async def play(ctx, *, query):
    '''
    Searches YouTube for the query and plays the first result in the voice channel.
    Usage: n!play [query]
    '''
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()

    def get_youtube_link(query):
        try:
            search = Search(query)
            first_result = search.results[0]
            return first_result.watch_url
        except Exception as e:
            print(f"Error searching for video: {e}")
            return None

    video_url = get_youtube_link(query)

    try:
        with yt_dlp.YoutubeDL(ytdl_format) as ydl:
            info = ydl.extract_info(video_url, download=False)
            filename = ydl.prepare_filename(info)
            print(video_url)
            await ctx.send("Downloading... This might take a while depending on the video length")
            ydl.download([video_url])
    except Exception as e:
        await ctx.send(f"An error occurred: (Downloading phase): {e}")
        return

    try:
        source = discord.FFmpegOpusAudio(executable="ffmpeg", source=filename, options=volume)
        source.read()
        ctx.voice_client.play(source)
        await ctx.send(f"Currently playing: [{info['title']}]"+f"(<{video_url}>)")
        os.remove(filename)
    except Exception as e:
        await ctx.send(f"An error occurred: (Playing phase): {e}")

@bot.command()
async def kill(ctx):
    '''
    Use to kill bot
    '''
    exit()

bot.run(DISCORD_BOT_TOKEN)