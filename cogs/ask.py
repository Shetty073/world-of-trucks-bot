import discord
from discord.ext import commands
import json
import os.path


class Ask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Get the help menu
    @commands.command()
    async def ask(self, ctx):
        with open(f"{os.path.dirname(__file__)}/../ask.json", 'r') as f:
            ask_content = json.load(f)

        ask_embed = discord.Embed(
            title="Bot developer: AlphaSierra",
            type="rich",
            description="",
            colour=discord.Color.gold()
        )
        ask_embed.set_author(name="World of Trucks Bot help menu",
                             icon_url="https://i.imgur.com/8cRyoSz.jpg")
        for k, v in ask_content.items():
            ask_embed.add_field(name=f"{k}",
                                value=f"{v}\n\n", inline=False)
        async with ctx.channel.typing():
            await ctx.send(embed=ask_embed)


def setup(bot):
    bot.add_cog(Ask(bot))
