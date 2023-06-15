import csv

import requests
from bs4 import BeautifulSoup

base_url = "https://www.mlb.com/stats/american-league/hits/2022?page="

page_num = 1
rows = []

while len(rows) < 101:
    print(page_num)
    url = base_url + str(page_num)
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")

    if page_num == 1:
        headers = [th.text for th in table.find_all("th")]

    rows.extend(
        [[td.text for td in tr.find_all("td")] for tr in table.find_all("tr")[1:]]
    )

    page_num += 1


with open("mlb_stats.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows[:100])
