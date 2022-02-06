# -*- coding: utf-8 -*-
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

import os
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

bot = commands.Bot(command_prefix="$")

@bot.event
async def on_ready():
    logger.info("Bot is ready")

@bot.event
async def on_message(message):
    if message.author != bot.user:
        if message.content.startswith('$'):
            await bot.process_commands(message)
        else:
            await message.channel.send(f"Hi %s! Ich bin Bubblestitch, dein Fake News Agent!" % message.author)
    
@bot.command()
async def test(ctx):
    await ctx.send('Das war ein Test')

bot.run(os.getenv('BOT_TOKEN'))