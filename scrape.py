import csv

import requests
from bs4 import BeautifulSoup

# 年度を選択
season = 2019
# リーグの選択(True:A_league False:N_league)
AorN = False
# ページ数選択(1ページ当たり25名)
pages = 4

if AorN:
    league_name = "american-league"
    csv_file = open("A_league_" + str(season) + ".csv", "w", newline="")
else:
    league_name = "national-league"
    csv_file = open("N_league_" + str(season) + ".csv", "w", newline="")


csv_writer = csv.writer(csv_file)


header = [
    "順位",
    "選手名",
    "Date",
    "Home Tm",
    "Away Tm",
    "PA",
    "AB",
    "R",
    "H",
    "2B",
    "3B",
    "HR",
    "RBI",
    "BB",
    "SO",
    "SB",
    "CS",
    "HBP",
    "AVG",
    "OBP",
    "SLG",
    "OPS",
]
csv_writer.writerow(header)
for page in range(1, pages + 1):
    if page == 1:
        url = "https://www.mlb.com/stats/" + league_name + "/hits/" + str(season)
        rank = 0
    else:
        url = (
            "https://www.mlb.com/stats/"
            + league_name
            + "/hits/"
            + str(season)
            + "?page="
            + str(page)
        )
        rank = (page - 1) * 25

    response = requests.get(url)
    content = response.content

    soup = BeautifulSoup(content, "html.parser")
    table = soup.find("table")

    rows = table.find_all("tr")
    count = 0

    for row in rows[1:26]:
        rank += 1
        player_name = row.find("a")["aria-label"]
        player_id = row.find("a")["href"].split("/")[2]
        player_url = (
            "https://baseballsavant.mlb.com/savant-player"
            + "/"
            + str.lower("-".join(player_name.split(" ")))
            + "-"
            + row.find("a")["href"].split("/")[2]
            + "?stats=gamelogs-r-hitting-mlb&season="
            + str(season)
        )

        # Send a GET request to the webpage
        url = player_url
        response = requests.get(url)

        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the table that contains the player data
        table_div = soup.find("div", {"id": "gamelogs-mlb"})

        table = table_div.table

        rows1 = table.tbody.find_all("tr")
        for row1 in rows1[1:]:
            columns = row1.find_all("td")
            data = [column.text.strip() for column in columns]

            if not (data[0].startswith("2")):
                continue
            row_data = [
                rank,  # 順位
                player_name,
                data[0].strip(),
                data[1].strip(),  # 自チーム
                data[2].strip(),  # 相手チーム
                data[3].strip(),  # 打席数
                data[4].strip(),  # 打数
                data[5].strip(),  # 安打数
                data[6].strip(),  # 打点
                data[7].strip(),  # 本塁打
                data[8].strip(),  # 四球
                data[9].strip(),  # 盗塁
                data[10].strip(),  # 出塁率
                data[11].strip(),
                data[12].strip(),
                data[13].strip(),
                data[14].strip(),
                data[15].strip(),
                data[16].strip(),
                data[17].strip(),
                data[18].strip(),
                data[19].strip(),
            ]

            csv_writer.writerow(row_data)


csv_file.close()
