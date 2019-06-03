# https://www.worldoftrucks.com/en/profile/846806

import requests as req
from bs4 import BeautifulSoup as Bs


def start(user_id):
    url = "https://www.worldoftrucks.com/en/profile/"
    res = req.get(url + user_id).content
    res_bs = Bs(res, "html.parser")

    # Profile name and image
    profile_inf = res_bs.find("a", {"title": "View user profile"})
    profile_name = profile_inf.find("img")["alt"]
    profile_image = profile_inf.find("img")["src"]
    # print(profile_name)
    # print(profile_image)

    # Profile country name and flag
    profile_nat = res_bs.find("div", {"class": "profile-frame"})
    profile_coun = profile_nat.find_all("img")[1]["alt"]
    profile_coun_img = "https://www.worldoftrucks.com" + profile_nat.find_all("img")[1]["src"]
    # print(profile_coun)
    # print(profile_coun_img)

    # Current rides
    profile_trucks_ets2 = res_bs.find_all("div", {"class": "gallery-item"})[0].find("div", {"class": "truck"})
    profile_trucks_ats = res_bs.find_all("div", {"class": "gallery-item"})[1].find("div", {"class": "truck"})

    # Truck names
    profile_truck_name_ets2 = profile_trucks_ets2.find("div", {"class": "name"}).string
    profile_truck_name_ats = profile_trucks_ats.find("div", {"class": "name"}).string

    # Current truck info
    profile_tr_det_ets2 = profile_trucks_ets2.find_all("div", {"class": "row"})
    profile_tr_det_ats = profile_trucks_ats.find_all("div", {"class": "row"})
    ets2_truck_data = {}  # ETS 2 current ride
    for item in profile_tr_det_ets2:
        key = item.find("div", {"class": "title"}).string
        value = item.find("div", {"class": "value"}).string
        if not value is None:
            ets2_truck_data[key] = value
        else:
            values = []
            value_0 = item.find("div", {"class": "value plates plates-eut2"}).find_all("img")[0]["src"]
            value_1 = item.find("div", {"class": "value plates plates-eut2"}).find_all("img")[1]["src"]
            ets2_truck_data["Plate front"] = f"https://www.worldoftrucks.com{value_0}"
            ets2_truck_data["Plate rear"] = f"https://www.worldoftrucks.com{value_1}"
    ats_truck_data = {}  # ATS current ride
    for item in profile_tr_det_ats:
        key = item.find("div", {"class": "title"}).string
        value = item.find("div", {"class": "value"}).string
        if not value is None:
            ats_truck_data[key] = value
        else:
            values = []
            value_0 = item.find("div", {"class": "value plates plates-ats"}).find_all("img")[0]["src"]
            value_1 = item.find("div", {"class": "value plates plates-ats"}).find_all("img")[1]["src"]
            ats_truck_data["Plate front"] = f"https://www.worldoftrucks.com{value_0}"
            ats_truck_data["Plate rear"] = f"https://www.worldoftrucks.com{value_1}"
    # for k, v in ets2_truck_data.items():
    #     print(f"{k} : {v}")
    # for k, v in ats_truck_data.items():
    #     print(f"{k} : {v}")

    # Global achievements
    glb_ach = res_bs.find("div", {"class": "achievements"}).find("div", {"class": "left"}).string
    glb_ach_percent = res_bs.find("div", {"class": "achievements"}).find("div", {"class": "right"}).string
    # print(glb_ach)
    # print(glb_ach_percent)

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
                                                                         {"class": "value value-kilometer"}).string
    tot_dis_unt = res_bs.find("div", {"class": "stat stat-total_dist"}).find("span",
                                                                             {"class": "unit unit-kilometer"}).string
    total_dist = f"{tot_dis} {tot_dis_unt.capitalize()}"  # Total distance


start(user_id="846806")
