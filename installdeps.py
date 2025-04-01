import subprocess
import sys

required_packages = [
    "discord.py",
    "requests",
    "nest_asyncio"
]

for package in required_packages:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
