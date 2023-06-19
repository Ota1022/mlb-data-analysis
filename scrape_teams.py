import requests
import csv
from bs4 import BeautifulSoup
import re

def keep_middle_letters(text):
    pattern = re.compile(r'[^a-zA-Z]+')
    result = re.sub(pattern, ' ', text)
    return result.strip()
StartSeason = 2011
EndSeason = 2023

for season in range(StartSeason, EndSeason+1):
    print(season)
    csv_file = open("A_league_team" + str(season) + ".csv", "w", newline="")
    csv_writer = csv.writer(csv_file)
    url = 'https://www.mlb.com/braves/stats/team/pitching/american-league/hits-allowed/'+str(season-1)+'?sortState=asc'
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
