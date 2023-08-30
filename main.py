import discord
from discord.ext import commands
from config import settings
import json

intents = discord.Intents.default().all()
intents.message_content = True
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)

welcome_message = 'Hello'


def load_message_file():
    try:
        with open('message.json', 'r') as message_file:
            return json.load(message_file)
    except FileNotFoundError:
        return {"welcome_message": "Добро пожаловать на сервер!"}


def save_message_file(message):
    with open('message.json', 'w') as message_file:
        json.dump(message, message_file, indent=4)


message = load_message_file()


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel is not None:
        await channel.send(message["welcome_message"])


@bot.command()
async def change(ctx, *, new_message: str):
    message["welcome_message"] = new_message
    save_message_file(message)
    await ctx.send(f'Приветственное сообщение изменено на: {new_message}')


bot.run(settings['token'])
