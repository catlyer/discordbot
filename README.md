your own discord bot which talks to you

Has three versions, old version can play music, openrouter version is the ai chatbot you want BUT ratelimited to 50 a day or 10 a hour. Ollama version is the same as openrouter, but runs locally and thus has no rate limit

Prerequisites: Some basic knowledge on how to make a discord bot token (for all versions), make an openrouter api key (for the openrouter version) and how to set up Ollama (for the ollama version)

How to install:
1. `git clone https://github.com/catlyer/discordbot.git` to clone this repo for yourself
2. RUN `installdeps.py` to install dependencies
3. EDIT `config.py` with the API keys, bot tokens, system prompt etc
4. Run `main.py` to start the bot

instructions to run apply for all three versions