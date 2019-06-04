import discord
from discord.ext import commands
import requests as req
from bs4 import BeautifulSoup as Bs


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Get driver data
    @commands.command()
    async def info(self, ctx, user_id="0"):
        try:
            # Profile name and image
            url = "https://www.worldoftrucks.com/en/profile/"
            res = req.get(url + user_id).content
            res_bs = Bs(res, "html.parser")
            profile_inf = res_bs.find("a", {"title": "View user profile"})
            profile_name = profile_inf.find("img")["alt"]
            profile_image = profile_inf.find("img")["src"]

            # Profile country name and flag
            profile_nat = res_bs.find("div", {"class": "profile-frame"})
            profile_coun = profile_nat.find_all("img")[1]["alt"]
            profile_coun_img = "https://www.worldoftrucks.com" + profile_nat.find_all("img")[1]["src"]

            # Current rides
            profile_trucks_ets2 = res_bs.find_all("div", {"class": "gallery-item"})[0].find("div", {"class": "truck"})
            profile_trucks_ats = res_bs.find_all("div", {"class": "gallery-item"})[1].find("div", {"class": "truck"})

            # Truck names
            profile_truck_name_ets2 = profile_trucks_ets2.find("div", {"class": "name"}).string
            profile_truck_name_ats = profile_trucks_ats.find("div", {"class": "name"}).string

            # Current truck info
            profile_tr_det_ets2 = profile_trucks_ets2.find_all("div", {"class": "row"})
            profile_tr_det_ats = profile_trucks_ats.find_all("div", {"class": "row"})
            ets2_plates = []  # ETS 2 plates
            ets2_tr_data = f"{profile_truck_name_ets2}\n"  # ETS 2 current ride
            for item in profile_tr_det_ets2:
                key = item.find("div", {"class": "title"}).string
                value = item.find("div", {"class": "value"}).string
                if value is not None:
                    ets2_tr_data += f"{key}: {value}\n"
                else:
                    value_0 = item.find("div", {"class": "value plates plates-eut2"}).find_all("img")[0]["src"]
                    value_1 = item.find("div", {"class": "value plates plates-eut2"}).find_all("img")[1]["src"]
                    ets2_plates.append(f"https://www.worldoftrucks.com{value_0}")
                    ets2_plates.append(f"https://www.worldoftrucks.com{value_1}")
            ats_plates = []  # ATS plates
            ats_tr_data = f"{profile_truck_name_ats}\n"  # ATS current ride
            for item in profile_tr_det_ats:
                key = item.find("div", {"class": "title"}).string
                value = item.find("div", {"class": "value"}).string
                if value is not None:
                    ats_tr_data += f"{key}: {value}\n"
                else:
                    value_0 = item.find("div", {"class": "value plates plates-ats"}).find_all("img")[0]["src"]
                    value_1 = item.find("div", {"class": "value plates plates-ats"}).find_all("img")[1]["src"]
                    ats_plates.append(f"https://www.worldoftrucks.com{value_0}")
                    ats_plates.append(f"https://www.worldoftrucks.com{value_1}")

            # Global achievements
            glb_ach_num = res_bs.find("div", {"class": "achievements"}).find("div", {"class": "left"}).string
            glb_ach_percent = res_bs.find("div", {"class": "achievements"}).find("div", {"class": "right"}).string

            # Global statistics
            jbs_cmp = res_bs.find("span", {"class": "value value-jobs"}).string  # Jobs accomplished
            jbs_wgt = res_bs.find("span", {"class": "value value-ton"}).string
            jbs_wgt_unt = res_bs.find("span", {"class": "unit unit-ton"}).string
            mass_transported = f"{jbs_wgt} {jbs_wgt_unt}"  # Total mass transported

            tm_hrs = res_bs.find("span", {"class": "value value-hour"}).string
            tm_hrs_unt = res_bs.find("span", {"class": "unit unit-hour"}).string
            tm_min = res_bs.find("span", {"class": "value value-minute"}).string
            tm_min_unt = res_bs.find("span", {"class": "unit unit-minute"}).string
            time_on_duty = f"{tm_hrs}{tm_hrs_unt} {tm_min}{tm_min_unt}"  # Time on duty

            avg_dis = res_bs.find("span", {"class": "value value-kilometer"}).string
            avg_dis_unt = res_bs.find("span", {"class": "unit unit-kilometer"}).string
            avg_del_dis = f"{avg_dis} {avg_dis_unt.capitalize()}"  # Average delivery distance

            tot_dis = res_bs.find("div", {"class": "stat stat-total_dist"}).find("span",
                                                                                 {
                                                                                     "class": "value value-kilometer"}).string
            tot_dis_unt = res_bs.find("div", {"class": "stat stat-total_dist"}).find("span",
                                                                                     {
                                                                                         "class": "unit unit-kilometer"}).string
            total_dist = f"{tot_dis} {tot_dis_unt.capitalize()}"  # Total distance
            glb_sts = f"Jobs accomplished: {jbs_cmp}\nTotal mass transported: {mass_transported}\nTime on duty: {time_on_duty}\nAverage delivery distance: {avg_del_dis}\nTotal distance covered: {total_dist}"

            # Info embed
            info_embed = discord.Embed(
                title="",
                type="rich",
                description="",
                color=discord.Color.gold()
            )
            info_embed.set_author(name=f"Statistics of {profile_name} from {profile_coun}", icon_url=profile_coun_img)
            info_embed.add_field(name="Current ETS 2 truck info", value=ets2_tr_data, inline=False)
            info_embed.add_field(name="Current ATS truck info", value=ats_tr_data, inline=False)
            info_embed.add_field(name="Global statistics", value=glb_sts, inline=False)
            info_embed.add_field(name=glb_ach_num,
                                 value=f"{glb_ach_percent} completed", inline=False)
            async with ctx.channel.typing():
                await ctx.send(embed=info_embed)
        except AttributeError:
            async with ctx.channel.typing():
                await ctx.send("Invalid user ID!\nUser ID must be a sequence of numbers.\nType `?ask` for more info..")


def setup(bot):
    bot.add_cog(Info(bot))
