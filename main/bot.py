import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True

token = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix='/', intents=intents)


class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("Livro de Magias..."))
    print(f'{bot.user.name} is logged in.')


@bot.event
async def setup_hook():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"Loaded Cog: {filename[:-3]}")


bot.run(token)
