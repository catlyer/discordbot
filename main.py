import discord
import requests
import json
import time

import nest_asyncio
nest_asyncio.apply()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

from config import OPENROUTER_API_KEY, OPENROUTER_MODEL, SYSTEM_PROMPT, DISCORD_BOT_TOKEN

# Used to check if the bot is logged in
@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

# guh
@client.event
async def on_message(message):
    time.sleep(1)
    if message.author == client.user:
        return  # Don't reply to yourself (but remove this for insane funnies + getting ratelimited)

    question = message.content
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": OPENROUTER_MODEL,
                "messages":[
                {"role": "user", "content": question},
                {"role": "system", "content": SYSTEM_PROMPT},
                ]
                })
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        result = response.json()
        print(result)
        answer = result['choices'][0]['message']['content']
        print(answer)
        await message.channel.send(answer)
    except Exception as e:
        await message.channel.send(f"Error: {e}")

client.run(DISCORD_BOT_TOKEN)