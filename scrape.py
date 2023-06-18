import requests
import csv
from bs4 import BeautifulSoup

# リーグの選択(True:A_league False:N_league)
AorN = False
# 年度を選択
StartSeason = 2011
EndSeason = 2023

for season in range(StartSeason, EndSeason+1):
    if AorN:
        league_name = "american-league"
        csv_file = open("A_league_" + str(season) + ".csv", "w", newline="")
    else:
        league_name = "national-league"
        csv_file = open("N_league_" + str(season) + ".csv", "w", newline="")

    csv_writer = csv.writer(csv_file)

    header = [
        "順位", #rank
        "選手名",#name
        "age",#年齢
        "debut_year",#デビュー
        "tall",#身長
        "weight",#体重
        "pro_year",#ドラフト
        "position",#ポジション
        "bt",#利き打ち/投げ
        "Date",#試合日
        "Home Tm",#ホームグラウンド
        "Away Tm",#ビジターグラウンド
        "PA",#打席数
        "AB",#打数
        "R",#得点
        "H",#安打
        "2B",#２塁打
        "3B",#３塁打
        "HR",#本塁打
        "RBI",#打点
        "BB",#四球
        "SO",#三振
        "SB",#盗塁
        "CS",#盗塁失敗
        "HBP",#死球
        "AVG",#打率
        "OBP",#出塁率
        "SLG",#長打率
        "OPS",#打撃指標数
        "SS", #SprintSpeed
        "HP2F"#HP to First
    ]
    csv_writer.writerow(header)
    # top100を選択(1ページ当たり25名)
    for page in range(1, 5):
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
                + player_id
                + "?stats=gamelogs-r-hitting-mlb&year="
                +str(season)
            )
            response_year = requests.get(url_year)
            soup_year = BeautifulSoup(response_year.content, "html.parser")

            tables_year = soup_year.find("div", {"class": "player-bio"}).find("ul")
            for year in tables_year.text.split("\n"):
                if "Debut" in year:
                    debut_year = year.split(":")[-1]
        

            if season >2014 :
                url_ss = (
                            "https://baseballsavant.mlb.com/savant-player/"
                            + str.lower("-".join(player_name.replace(".", "").split(" ")))
                            + "-"
                            + player_id
                            + "?stats=statcast-r-running-mlb") 
                response_ss = requests.get(url_ss)
                soup_ss = BeautifulSoup(response_ss.content,"html.parser" )
                div =soup_ss.find('div',{"id":"statcastRunning"})           
                tables_ss = div.find("div",{"class":"table-savant"}).find("tbody")

                trr = tables_ss.find_all('tr')
                for i in range(0,len(trr)):
                    if trr[i].text.split('\n')[1] ==" " +str(season):
                        sprintspeed_row = trr[i].text.split('\n')[3].split(" ")[1]
                        if sprintspeed_row == '':
                            sprintspeed = None
                        else:
                            sprintspeed = float(sprintspeed_row)
                        hp2f_row = trr[i].text.split('\n')[4].split(" ")[1]
                        if hp2f_row == '':
                            hp2f = None
                        else:
                            hp2f = float(hp2f_row)
            else:
                sprintspeed = None
                hp2f = None        
            
                
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
            age = table_new[10]
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
                    rank, 
                    player_name,
                    age,
                    debut_year,
                    tall,
                    weight,
                    pro_year,
                    position,
                    bt,
                    data[0].strip(),
                    data[1].strip(),  
                    data[2].strip(),  
                    data[3].strip(),  
                    data[4].strip(),  
                    data[5].strip(),  
                    data[6].strip(),  
                    data[7].strip(),  
                    data[8].strip(),  
                    data[9].strip(),  
                    data[10].strip(),  
                    data[11].strip(),
                    data[12].strip(),
                    data[13].strip(),
                    data[14].strip(),
                    data[15].strip(),
                    data[16].strip(),
                    data[17].strip(),
                    data[18].strip(),
                    data[19].strip(),
                    sprintspeed,
                    hp2f
                ]

                csv_writer.writerow(row_data)

    csv_file.close()

# crawl team data
import re

def keep_middle_letters(text):
    pattern = re.compile(r'[^a-zA-Z]+')
    result = re.sub(pattern, ' ', text)
    return result.strip()
StartSeason = 2011
EndSeason = 2023

for season in range(StartSeason, EndSeason+1):
    csv_file = open("N_league_team" + str(season) + ".csv", "w", newline="")
    csv_writer = csv.writer(csv_file)
    url = 'https://www.mlb.com/stats/team/pitching/national-league/'+str(season)+'?sortState=asc'
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    table=soup.find('table',{'class':'bui-table is-desktop-sKqjv9Sb'})
    rows1 = table.tbody.find_all('tr')
    for row1 in rows1[0:]:
        columns = row1.find_all('td')
        data=[column.text.strip() for column in columns]
        text=row1.find('th').text.split('\u200c\u200c\u200c')[0]
        team=keep_middle_letters(text)
        row_data = [
                    team,
                    data[0].strip(),
                    data[1].strip(),  
                    data[2].strip(),  
                    data[3].strip(),  
                    data[4].strip(),  
                    data[5].strip(),  
                    data[6].strip(),  
                    data[7].strip(),  
                    data[8].strip(),  
                    data[9].strip(),  
                    data[10].strip(),  
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
