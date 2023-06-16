import csv

import requests
from bs4 import BeautifulSoup

# リーグの選択(True:A_league False:N_league)
AorN = False
# 年度を選択
for season in range(2011, 2023):
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
        "age",
        "debut_year",
        "tall",
        "weight",
        "pro_year",
        "position",
        "bt",
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
    # top100を選択
    for page in range(1, 4):
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

        # Create a BeautifulSoup object to parse the HTML content

        response = requests.get(url)
        content = response.content

        soup = BeautifulSoup(content, "html.parser")
        table = soup.find("table")

        rows = table.find_all("tr")

        for row in rows[1:26]:
            rank += 1
            player_name = row.find("a")["aria-label"]
            player_id = row.find("a")["href"].split("/")[2]
            print(player_name)

            player_url = (
                "https://baseballsavant.mlb.com/savant-player"
                + "/"
                + str.lower("-".join(player_name.replace(".", "").split(" ")))
                + "-"
                + player_id
                + "?stats=gamelogs-r-hitting-mlb&season="
                + str(season)
            )
            url_year = (
                "https://www.mlb.com/player/"
                + str.lower("-".join(player_name.replace(".", "").split(" ")))
                + "-"
                + player_id
                + "?stats=gamelogs-r-hitting-mlb&year=2019"
            )
            response_year = requests.get(url_year)
            soup_year = BeautifulSoup(response_year.content, "html.parser")

            tables_year = soup_year.find("div", {"class": "player-bio"}).find("ul")
            for year in tables_year.text.split("\n"):
                if "Debut" in year:
                    debut_year = year.split(":")[-1]

            # Send a GET request to the webpage
            url = player_url
            response = requests.get(url)

            # Create a BeautifulSoup object to parse the HTML content
            soup = BeautifulSoup(response.content, "html.parser")

            tables = soup.find("div", {"class": "bio-player-name"}).find_all("div")
            table1 = tables[1]
            table_new = table1.text.split()
            tall = (
                float(table_new[5].replace("'", "")) * 30.48
                + float(table_new[6].replace('"', "")) * 2.54
            )
            age = int(table_new[10]) - (2023 - season)
            position = table_new[0]
            bt = table_new[3]
            weight = float(table_new[7].replace("LBS", "")) * 453.6 / 1000
            if tables[2].a:
                pro_year = int(tables[2].a.text)
            else:
                pro_year = 0
            # Find the table that contains the player data
            table_div = soup.find("div", {"id": "gamelogs-mlb"})
            if not bool(table_div.find("tbody")):
                print(player_name + ":はデータが存在しません")
                continue
            table = table_div.table

            rows1 = table.tbody.find_all("tr")
            for row1 in rows1[0:]:
                columns = row1.find_all("td")
                data = [column.text.strip() for column in columns]

                if not (data[0].startswith("2")):
                    continue
                row_data = [
                    rank,  # 順位
                    player_name,
                    age,
                    debut_year,
                    tall,
                    weight,
                    pro_year,
                    position,
                    bt,
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
