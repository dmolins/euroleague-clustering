import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

def order_name(row):
    if isinstance(row.player, str) and row.player != '':
        p = row.player.split(', ')
        if len(p) > 1:
            row.player = p[1] + ' ' + p[0]

    return row

url = 'https://www.euroleague.net/competition/players?listtype=alltime'
players = pd.DataFrame(columns=['player','height','position','year_born','nationality'])

req = requests.get('https://www.euroleague.net/competition/players?listtype=alltime')
soup = bs(req.text, 'html.parser')

letters_container = soup.find(id='ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_ctl01_divAlphabetContainer')
letters = letters_container.find_all('a')

for letter in letters:
    #print(letter)
    req2 = requests.get('https://www.euroleague.net' + letter['href'])
    soup2 = bs(req2.text, 'html.parser')
    players_container = soup2.find('div', attrs={'class', 'items-list'})
    link_players = players_container.find_all('a')
    
    for player in link_players:
        req3 = requests.get('https://www.euroleague.net' + player['href'])
        soup3 = bs(req3.text, 'html.parser')
        data = soup3.find("div", {"class": "player-data"})
        player = data.find("div", {"class": "name"}).text
        pos = data.find("div", {"class": "summary-first"}).text.split('\n')
        if len(pos)>3:
            position = pos[4]
        else:
            position = ''
        info_arr = data.find("div", {"class": "summary-second"}).text.split('\n')
        height = year_born = nacionality = ''
        for info in info_arr:
            if 'Height' in info:
                height = info.split(': ')[1]
            elif 'Born' in info:
                year_born = info.split(', ')[1]
            elif 'Nationality' in info:
                nacionality = info.split(': ')[1]

        players = players.append({'player': player, 'height': height, 'position': position, 'year_born': year_born, 'nationality': nacionality}, ignore_index=True)

new_players = players.apply(order_name, axis='columns')
new_players.to_csv('/Users/dmolins/Desktop/david/uni/TFG/data/players_info.csv', sep=';', index = False)
