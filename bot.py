import discord
from discord.ext import commands
import configparser

# Get the token from configuration file
config = configparser.ConfigParser()
config.read("config/config.ini")
TOKEN = config["BOT"]["token"]

# Bot code begins
bot = commands.Bot(command_prefix='?', description="just `.ask` for help", case_insensitive=True)


# Message on terminal when the bot starts
@bot.event
async def on_ready():
    print(bot.user.name)
    print("Bot running..")
    await bot.change_presence(activity=discord.Game("just ?ask for help"))


# Cogs list
extensions = ["cogs.info"]

# Load all cogs
if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f"{extension} loaded..")
        except Exception as error:
            print(f"ERROR: {extension} could not be loaded. {error}")

bot.remove_command("help")  # Remove the default help command
bot.run(TOKEN)
