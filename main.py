# -*- coding: utf-8 -*-
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

import os
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
from model import FakeNewsAgent
import validators
load_dotenv(find_dotenv())

# Instantiate model with endpoint
agent = FakeNewsAgent(endpoint_url=os.getenv('ENDPOINT_URL'))

# Instantiate bot
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
            response = f"Hi {message.author}! Ich bin Bubblestitch, dein Fake News Agent! " \
            "Du kannst mich verwenden, um News Artikel (auf Deutsch!) hinsichtlich Fake News " \
            "bewerten zu lassen. Dazu verwende einfach das Kommando '$score <URL zum Artikel>' " \
            "mit einer URL zu einem Artikel. Ich liefere dir einen Fake-Score zurück, welcher zwischen 0 und 1 liegt. " \
            "Je höher der Score sich bei 1 befindet, desto eher geht meine Einschätzung davon aus, dass der "\
            "Artikel den du mir gegeben hast Fake News beinhaltet. Versuchs doch einfach!"
            
            await message.channel.send(response)
    
@bot.command()
async def score(ctx, url):
    # Check if url is valid
    if not validators.url(str(url)):
        # Generate response
        response = "Sorry, aber das war keine gültige URL! Check nochmal deine Eingabe und versuchs nochmal!"
        logger.info(f"'{url}' war keine gültige URL")
    else:
        logger.info(f"Got {url} to score")
        # Feed endpoint with url and get fake score
        raw = agent.predict(url)
        fake_score = round(raw['data'][0][1], 2)
        # Generate som interpretations for the user
        if fake_score < 0.4:
            interpretation_str = "Der Artikel sieht für mich nicht nach Fake News aus."
        elif fake_score >= 0.4 and fake_score <= 0.8:
            interpretation_str = "Der Artikel könnte Fake sein, bin mir aber nicht sicher." 
        elif fake_score > 0.8:
            interpretation_str = "Hey Achtung, das sieht nach Fake News aus!"

        # Generate response
        response = f"Dieser Artikel hat einen Fake-Score von {fake_score}. {interpretation_str}"

    await ctx.send(response)

bot.run(os.getenv('BOT_TOKEN'))