# Reference: https://dev.to/codesphere/create-a-discord-bot-in-minutes-with-python-2jgp
#            DiscordDatabase | https://pypi.org/project/DiscordDatabase/#:~:text=Discord%20Database,text%20channel%20that%20you%20specify.

import discord
from discord.ext import commands, tasks
from DiscordDatabase import DiscordDatabase
from datetime import datetime
import random

TOKEN = "MTE2ODMxNTkzNzIyMTUyOTYwMA.Gu-KPX.ZM-TMMMSS_EiofYDyBram2n-dLzFW1zQPCrEsY"
DB_GUILD_ID = 801648529310482462

intents = discord.Intents.default()
intents.messages = True

# Initialize Bot and Denote The Command Prefix
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

db = DiscordDatabase(bot, DB_GUILD_ID)

# Runs when Box Successfully Connects
@bot.event
async def on_ready():
    print(f'{bot.user} successfully logged in!')
    global database
    database = await db.new("database", "quote")
    time_module.start()

@bot.event
async def on_message(message):
    # Make sure the Bot doesn't respond to it's own messages
    if message.author == bot.user: 
        return
    
    if message.content == 'hello':
        await message.channel.send(f'Hi {message.author}')
    if message.content == 'bye':
        await message.channel.send(f'Goodbye {message.author}')

    await bot.process_commands(message)

@bot.command()
async def add_quote(ctx, *args):
  quotes = await database.get("quotes")
  quote = f"> _{' '.join(args)}_"
  if(not quotes):
    await database.set("quotes", [quote])
  else:
    quotes.append(quote)
    await database.set("quotes", quotes)
  await ctx.send(quote)

@bot.command()
async def quote(ctx):
  quotes = await database.get("quotes")
  if (not quotes): await ctx.send('No quote available')
  await ctx.send(random.choice(quotes))

async def get_random_quote():
  quotes = await database.get("quotes")
  if (not quotes): return
  return random.choice(quotes)

@tasks.loop(seconds=5)
async def time_module():
  current_time = datetime.now().strftime("%H:%M:%S")
  if current_time == "06:00:00":
    channel = bot.get_channel(801648529310482465)
    random_quote = await get_random_quote()
    if(random_quote):
      await channel.send(random_quote)

bot.run(TOKEN)