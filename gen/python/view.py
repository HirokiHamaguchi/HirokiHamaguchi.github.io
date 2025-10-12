import math
import os

import requests


def print_view(dirname: str):
    USER_ID = "hari64"
    PER_PAGE = 20
    allViews = 0
    allLikes = 0
    allStocks = 0

    with open(os.path.join(dirname, "qiitaToken")) as f:
        KEY = f.readline().strip()

    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer " + KEY,
    }

    url = "https://qiita.com/api/v2/users/" + USER_ID
    res = requests.get(url, headers=headers)
    json_qiita_info = res.json()

    items_count = json_qiita_info["items_count"]

    page = math.ceil(items_count / PER_PAGE)

    print("|記事タイトル|いいね数|ストック数|View数|")

    for i in range(page):
        url = (
            "https://qiita.com/api/v2/authenticated_user/items" + "?page=" + str(i + 1)
        )
        res = requests.get(url, headers=headers)
        json_qiita_info = res.json()

        for j in range(len(json_qiita_info)):
            item_id = json_qiita_info[j]["id"]

            url = "https://qiita.com/api/v2/items/" + str(item_id)
            res = requests.get(url, headers=headers)
            json_view = res.json()

            page_view = json_view["page_views_count"]
            allViews += page_view
            allLikes += json_qiita_info[j]["likes_count"]
            allStocks += json_qiita_info[j]["stocks_count"]

            print(
                "| "
                + json_qiita_info[j]["title"]
                + " | "
                + str(json_qiita_info[j]["likes_count"])
                + " |"
                + str(json_qiita_info[j]["stocks_count"])
                + " |"
                + str(page_view)
                + " |"
            )

    averageLikes = round(allLikes / items_count, 1)
    averageStocks = round(allStocks / items_count, 1)
    engagementRate = round(allLikes / allViews * 100, 2)
    print("View総計:" + str(allViews))
    print("平均いいね数:" + str(averageLikes))
    print("平均ストック数:" + str(averageStocks))
    print("平均いいね率:" + str(engagementRate) + "%")
    print("正常出力完了")
