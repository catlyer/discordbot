import discord
import time
from ollama import chat, ChatResponse
import json

import nest_asyncio
nest_asyncio.apply()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

from config import OLLAMA_MODEL, SYSTEM_PROMPT, DISCORD_BOT_TOKEN

systemprompt = SYSTEM_PROMPT # maybe this helps with the schizoing out?

# ACTUAL BOT SHIT
# doing everything in a single file is the worst way to do this shit but idc we ball

# Used to check if the bot is logged in
@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

# guh
@client.event
async def on_message(message):
    time.sleep(3) # limit becase
    if message.author == client.user:
        return 
    
    #user = message.author  
    question = message.content
    #print(user)
    #print(question)

    prompt = question
    print("prompt:" + prompt)

    try:
        response: ChatResponse = chat(model=OLLAMA_MODEL, messages=[
            {
                'role': 'system',
                'content': systemprompt,
            },

            {
                'role': 'user',
                'content': prompt,
            },
        ]
        )
        answer = response['message']['content']
        final = answer
        print(final)
        await message.channel.send(final)
    except Exception as e:
        await message.channel.send(f"Error: {e}")

client.run(DISCORD_BOT_TOKEN)   