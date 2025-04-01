import subprocess
import sys

required_packages = [
    "discord.py",
    "PyNaCl",
    "requests",
    "pytubefix",
    "yt-dlp",
    "nest_asyncio"
]

for package in required_packages:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
