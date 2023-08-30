import discord
from discord.ext import commands
from config import settings
import json

intents = discord.Intents.default().all()
intents.message_content = True
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)


def load_message_file():
    try:
        with open('message.json', 'r') as message_file:
            return json.load(message_file)
    except FileNotFoundError:
        return {"welcome_message": "Hello, {user}!"}


def save_message_file(message):
    with open('message.json', 'w') as message_file:
        json.dump(message, message_file, indent=4)


message = load_message_file()


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have sufficient rights to execute this command.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("No such command found.")
    else:
        print(error)


@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel is not None:
        welcome_message = message["welcome_message"].format(user=member.mention)
        await channel.send(welcome_message)


@bot.command()
@commands.has_permissions(administrator=True)
async def change(ctx, *, new_message: str):
    """Changes the welcome message.

     Example usage: !change New welcome message.
     """
    message["welcome_message"] = new_message
    save_message_file(message)
    await ctx.send(f'The message has been changed to: {new_message}')


class HelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Command List", description="List of all available commands:")
        for cog, commands in mapping.items():
            if cog:
                cog_name = cog.qualified_name
                command_list = [f"`{command.name}`" for command in commands]
                command_text = '\n'.join(command_list)
                embed.add_field(name=cog_name, value=command_text, inline=False)
            else:
                command_list = [f"`{command.name}`" for command in commands]
                command_text = ' '.join(command_list)
                embed.description = command_text

        await self.get_destination().send(embed=embed)


bot.help_command = HelpCommand()

bot.run(settings['token'])
