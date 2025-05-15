import glob
import os

import getorg  # type: ignore
from geopy import Nominatim  # type: ignore


def talkmap(dirname: str):
    g = glob.glob(os.path.join(dirname, "_talks/*.md"))

    geo_coder = Nominatim(user_agent="hari64")
    location_dict = {}
    location = ""

    for file in g:
        with open(file, "r", encoding="utf-8") as f:
            lines = f.read()
            if lines.find('location: "') > 1:
                loc_start = lines.find('location: "') + 11
                lines_trim = lines[loc_start:]
                loc_end = lines_trim.find('"')
                location = lines_trim[:loc_end]

            location_dict[location] = geo_coder.geocode(location)
            print(location, "\n", location_dict[location])

    getorg.orgmap.create_map_obj()
    getorg.orgmap.output_html_cluster_map(
        location_dict,
        folder_name=os.path.join(dirname, "talkmap"),
        hashed_usernames=False,
    )
