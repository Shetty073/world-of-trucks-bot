import discord
from discord.ext import commands
import requests as req
from bs4 import BeautifulSoup as Bs


class Plates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Get plates
    @commands.command()
    async def plates(self, ctx, user_id="0"):
        try:
            # Current rides
            url = "https://www.worldoftrucks.com/en/profile/"
            res = req.get(url + user_id).content
            res_bs = Bs(res, "html.parser")
            profile_trucks_ets2 = res_bs.find_all("div", {"class": "gallery-item"})[0].find("div", {"class": "truck"})
            profile_trucks_ats = res_bs.find_all("div", {"class": "gallery-item"})[1].find("div", {"class": "truck"})

            # Current truck info
            profile_tr_det_ets2 = profile_trucks_ets2.find_all("div", {"class": "row"})
            profile_tr_det_ats = profile_trucks_ats.find_all("div", {"class": "row"})
            ets2_plates = []  # ETS 2 plates
            for item in profile_tr_det_ets2:
                key = item.find("div", {"class": "title"}).string
                value = item.find("div", {"class": "value"}).string
                if value is None:
                    value_0 = item.find("div", {"class": "value plates plates-eut2"}).find_all("img")[0]["src"]
                    value_1 = item.find("div", {"class": "value plates plates-eut2"}).find_all("img")[1]["src"]
                    ets2_plates.append(f"https://www.worldoftrucks.com{value_0}")
                    ets2_plates.append(f"https://www.worldoftrucks.com{value_1}")

            ats_plates = []  # ATS plates
            for item in profile_tr_det_ats:
                key = item.find("div", {"class": "title"}).string
                value = item.find("div", {"class": "value"}).string
                if value is None:
                    value_0 = item.find("div", {"class": "value plates plates-ats"}).find_all("img")[0]["src"]
                    value_1 = item.find("div", {"class": "value plates plates-ats"}).find_all("img")[1]["src"]
                    ats_plates.append(f"https://www.worldoftrucks.com{value_0}")
                    ats_plates.append(f"https://www.worldoftrucks.com{value_1}")

            # List of embeds
            embeds = []
            #  European plates
            plates_embed_ets2_front = discord.Embed(
                title="European front plate",
                type="rich",
                description="",
                color=discord.Color.gold()
            )
            plates_embed_ets2_front.set_image(url=ets2_plates[0])
            embeds.append(plates_embed_ets2_front)
            plates_embed_ets2_rear = discord.Embed(
                title="European rear plate",
                type="rich",
                description="",
                color=discord.Color.gold()
            )
            plates_embed_ets2_rear.set_image(url=ets2_plates[1])
            embeds.append(plates_embed_ets2_rear)

            # American plates
            plates_embed_ats_front = discord.Embed(
                title="American front plate",
                type="rich",
                description="",
                color=discord.Color.gold()
            )
            plates_embed_ats_front.set_image(url=ats_plates[0])
            embeds.append(plates_embed_ats_front)
            plates_embed_ats_rear = discord.Embed(
                title="American rear plate",
                type="rich",
                description="",
                color=discord.Color.gold()
            )
            plates_embed_ats_rear.set_image(url=ats_plates[1])
            embeds.append(plates_embed_ats_rear)

            # Finally send all the embeds
            for em in embeds:
                async with ctx.channel.typing():
                    await ctx.send(embed=em)
        except Exception:
            async with ctx.channel.typing():
                await ctx.send("Invalid user ID!\nUser ID must be a sequence of numbers.\nType `?ask` for more info..")


def setup(bot):
    bot.add_cog(Plates(bot))
