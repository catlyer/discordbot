import subprocess
import sys

required_packages = [
    "discord.py",
    "PyNaCl",
    "requests",
    "google-generativeai",
    "pytubefix",
    "yt-dlp",
    "nest_asyncio",
#    "pyttsx3",
]

for package in required_packages:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


import discord
from discord.ext import commands
from requests import get
import os
import google.generativeai as genai
import yt_dlp
import random
from pytubefix import Search
#import pyttsx3

global vol
vol = 50

import nest_asyncio
nest_asyncio.apply()

intents = discord.Intents.all()
prefix = "n!"
bot = commands.Bot(command_prefix=prefix,intents=intents)

genai.configure(api_key="Gemini_API_KEY")
model = genai.GenerativeModel("gemini-pro")

ytdl_format = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": False,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "default_search": "auto",
    "source_address": "0.0.0.0",}

# Used to check if the bot is logged in
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Command to join a VC
@bot.command()
async def join(ctx):
    """
    Used to make the bot join VC
    """
    # Check if the user is connected to a voice channel
    if not ctx.author.voice:
        await ctx.send("You are not connected to a voice channel.")
        return

    channel = ctx.author.voice.channel

    # Try connecting to the channel
    try:
        print("attempting to join vc")
        await ctx.author.voice.channel.connect()
        print("connecting to vc")
        await ctx.send(f"Joined {channel.name}")
        print("connected to vc")
    except discord.ClientException as e:
        await ctx.send(f"Failed to join voice channel: {e}")

# Command to leave VC
@bot.command()
async def leave(ctx):
    '''
    Used to make the bot leave a VC
    '''
    await ctx.voice_client.disconnect()

# Command to test latency
@bot.command()
async def ping(ctx):
    '''
    Used to test the latency of the bot
    '''
    latency = bot.latency
    await ctx.send(latency)

# Command for API calls to gemini
@bot.command()
async def gemini(ctx, *, gemini_prompt):
    '''
    Uses Gemini to get an response
    Usage: n!gemini [Prompt]
    '''
    try:
        response = model.generate_content([gemini_prompt, "Keep your responses STRICTLY under 2000 characters."])
        print(response.text)
        await ctx.send(f"Gemini: {response.text}")
    except Exception as e:
        await ctx.send(f"Error: {e}")

# Command to set volume
@bot.command()
async def volume(ctx, vol):
    """
    Used to set volume
    Usage: n!volume [Volume]
    Defaults to 50
    """
    global volume
    volume = f"-vol {vol}"
    await ctx.send(f"Set volume to {vol}")

# Command to play youtube video audio using URL
@bot.command()
async def linkplay(ctx, video_url):
    """
    Plays a YouTube video in the voice channel.
    Usage: n!linkplay [Url to youtube video]
    """
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()

    try:
        with yt_dlp.YoutubeDL(ytdl_format) as ydl:
            info = ydl.extract_info(video_url, download=False)
            filename = ydl.prepare_filename(info)
            await ctx.send("Downloading... This might take a while depending on the video length")
            ydl.download([video_url])
    except Exception as e:
        await ctx.send(f"Somebody tell <@1132156997358334093> that there is a problem with their code: (Downloading phase): {e}")
        return

    try:
        source = discord.FFmpegOpusAudio(executable="ffmpeg", source=filename, options=volume)
        source.read()
        ctx.voice_client.play(source)
        await ctx.send(f"Currently playing: [{info['title']}]"+f"(<{video_url}>)")
        os.remove(filename)
    except Exception as e:
        await ctx.send(f"Somebody tell <@1132156997358334093> that there is a problem with their code: (Playing phase): {e}")

@bot.command()
async def play(ctx, *, query):
    """
    Searches YouTube for the query and plays the first result in the voice channel.
    Usage: n!play [query]
    """
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
        await ctx.send(f"Somebody tell <@1132156997358334093> that there is a problem with their code: (Downloading phase): {e}")
        return

    try:
        source = discord.FFmpegOpusAudio(executable="ffmpeg", source=filename, options=volume)
        source.read()
        ctx.voice_client.play(source)
        await ctx.send(f"Currently playing: [{info['title']}]"+f"(<{video_url}>)")
        os.remove(filename)
    except Exception as e:
        await ctx.send(f"Somebody tell <@1132156997358334093> that there is a problem with their code: (Playing phase): {e}")

# Command for tts
@bot.command()
async def tts(ctx, *, text):
    """
    Converts text to speech and plays it in the voice channel.
    Usage: n!tts [text]
    Currently disabled because fuck everything that works in this world
    """
    #engine = pyttsx3.init()
    #engine.say(text)
    #engine.runAndWait()
    await ctx.send("TTS is currently disabled")

# Command to kill the bot
@bot.command()
async def kill(ctx):
    """
    Use to kill bot
    """
    exit()

bot.run("BOT_API_KEY")
