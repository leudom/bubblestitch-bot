import os
import discord
from discord.ext import commands

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

client = commands.Bot(command_prefix="!")
@client.event
async def on_ready():
    print("bot is ready")
@client.event
async def on_message(message):
    if message.author != client.user:
        await message.channel.send(f"Hi du! Ich bin Bubblestitch, dein Fake News Agent!")
client.run(os.getenv('BOT_TOKEN'))