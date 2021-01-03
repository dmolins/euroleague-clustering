from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd

first_time = True

year = 18
url = 'https://www.basketball-reference.com/international/euroleague/20{}.html'.format(year)

def get_links(teams):
    team_names = []
    links = []
    for t in teams:
        team_names.append(t.find("a").text)
        links.append(t.find("a")['href'])
    return (team_names, links)

def get_euroleague_table(container):
    for table in container:
        if table.get('id') == 'player_per_game-elg':
            return table

def get_season_stats(url, first_time, team, year):
    #opening up connection, grabbing the page
    uClient2 = uReq(url)
    page_html2 = uClient2.read()
    uClient2.close()
    
    #html parser
    page_soup = soup(page_html2, "html.parser")
    container = page_soup.findAll("table")
    
    table = get_euroleague_table(container)
    
    l = []
    for tr in table.tbody.find_all('tr'):
        th = tr.find_all('th')
        td = tr.find_all('td')
        row = [th[0].text]

        for tr in td:
            row.append(tr.text)
        row.append(team)
        row.append(year)
        l.append(row)
    
    df_add = pd.DataFrame(l, columns=header)
    
    return df_add, header


header = ['Player', 'G', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB', 
'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'Team', 'Season']
df = pd.DataFrame(columns=header)

#opening up connection, grabbing the page
uClient = uReq(url)
page_html = uClient.read()
uClient.close()

#html parser
page_soup = soup(page_html, "html.parser")

container = page_soup.find("table")
teams_html = container.tbody.find_all('tr')

(teams, links) = get_links(teams_html)

#agafar stats d'un equip
for i in range(len(teams)):
    df_add, header = get_season_stats('https://www.basketball-reference.com' + links[i], first_time, teams[i], year)
    df_concat = [df, df_add]
    df = pd.concat(df_concat)

df.to_csv('/Users/dmolins/Desktop/david/uni/TFG/data/season-stats/Euroleague_box-score_{}.csv'.format(year), 
          sep=';', header = header, index = False)