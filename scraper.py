import sys
import csv
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains as AC
from bs4 import BeautifulSoup as BS

# team offense @ http://www.espn.com/nfl/statistics/team/_/stat/total
# team defense @ http://www.espn.com/nfl/statistics/team/_/stat/total/position/defense
def scrapeNFLTeamStats(year=2018, offense=True):
    if offense:
        if year == 2018:
            url = 'http://www.espn.com/nfl/statistics/team/_/stat/total'
        else:
            url = 'http://www.espn.com/nfl/statistics/team/_/stat/total/year/{}'.format(year)
        outFileName = 'data/nfl/nfl_team_offense_{}.csv'.format(year)
    else:
        if year == 2018:
            url = 'http://www.espn.com/nfl/statistics/team/_/stat/total/position/defense'
        else:
            url = 'http://www.espn.com/nfl/statistics/team/_/stat/total/position/defense/year/{}'.format(year)
        outFileName = 'data/nfl/nfl_team_defense_{}.csv'.format(year)

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(chrome_options=options)

    try:
        driver.set_page_load_timeout(60)
        driver.get(url)
        wait = WebDriverWait(driver, 100)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tablehead')))
        html = driver.page_source

    except TimeoutException as ex:
        isrunning = 0
        print(str(ex))
        driver.close()
        sys.exit()

    driver.quit()

    soup = BS(html, 'html.parser')
    teamOTable = soup.find_all('table')[0]
    names = ['Rank','Tm', 'Yds', 'Yds/G', 'PYds', 'PYds/G', 'RYds', 'RYds/G', 'PTS', 'PTS/G']
    table = pd.DataFrame(columns=names, index=range(0,32))
    rows = teamOTable.find_all('tr')

    rowMarker = 0
    for i in range(1,len(rows)):
        colMarker = 0
        columns = rows[i].find_all('td')
        for column in columns:
            table.iat[rowMarker, colMarker] = column.get_text()
            colMarker += 1
        rowMarker += 1

    table.sort_values(by=['Tm'], inplace=True)
    table.drop('Rank', axis=1, inplace=True)
    table.to_csv(outFileName, index_label=False)

# team passing @ http://www.espn.com/nfl/statistics/team/_/stat/passing
# team pass D @ http://www.espn.com/nfl/statistics/team/_/stat/passing/position/defense
def scrapeNFLPassingStats(year=2018, offense=True):
    if offense:
        if year == 2018:
            url = 'http://www.espn.com/nfl/statistics/team/_/stat/passing'
        else:
            url = 'http://www.espn.com/nfl/statistics/team/_/stat/passing/year/{}'.format(year)
        outFileName = 'data/nfl/nfl_team_pass_offense_{}.csv'.format(year)
    else:
        if year == 2018:
            url = 'http://www.espn.com/nfl/statistics/team/_/stat/passing/position/defense'
        else:
            url = 'http://www.espn.com/nfl/statistics/team/_/stat/passing/position/defense/year/{}'.format(year)
        outFileName = 'data/nfl/nfl_team_pass_defense_{}.csv'.format(year)

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(chrome_options=options)

    try:
        driver.set_page_load_timeout(60)
        driver.get(url)
        wait = WebDriverWait(driver, 100)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tablehead')))
        html = driver.page_source

    except TimeoutException as ex:
        isrunning = 0
        print(str(ex))
        driver.close()
        sys.exit()

    driver.quit()

    soup = BS(html, 'html.parser')
    teamOTable = soup.find_all('table')[0]
    names = ['Rank','Tm', 'Attempts', 'Completions', 'Percentage', 'Yds', 'PYds/A', 'Long', 'TD', 'Int', 'Sacks', 'YdsL', 'Passer Rating', 'PYds/G']
    table = pd.DataFrame(columns=names, index=range(0,32))
    rows = teamOTable.find_all('tr')

    rowMarker = 0
    for i in range(1,len(rows)):
        colMarker = 0
        columns = rows[i].find_all('td')
        for column in columns:
            table.iat[rowMarker, colMarker] = column.get_text()
            colMarker += 1
        rowMarker += 1

    table.sort_values(by=['Tm'], inplace=True)
    table.drop(['Rank','Attempts','Completions','Long','Sacks','YdsL'], axis=1, inplace=True)
    table.to_csv(outFileName, index_label=False)

# team rushing @ http://www.espn.com/nfl/statistics/team/_/stat/rushing
# team rush D @ http://www.espn.com/nfl/statistics/team/_/stat/rushing/position/defense
def scrapeNFLRushingStats(year=2018, offense=True):
    if offense:
        if year == 2018:
            url = 'http://www.espn.com/nfl/statistics/team/_/stat/rushing'
        else:
            url = 'http://www.espn.com/nfl/statistics/team/_/stat/rushing/year/{}'.format(year)
        outFileName = 'data/nfl/nfl_team_rush_offense_{}.csv'.format(year)
    else:
        if year == 2018:
            url = 'http://www.espn.com/nfl/statistics/team/_/stat/rushing/position/defense'
        else:
            url = 'http://www.espn.com/nfl/statistics/team/_/stat/rushing/position/defense/year/{}'.format(year)
        outFileName = 'data/nfl/nfl_team_rush_defense_{}.csv'.format(year)

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(chrome_options=options)

    try:
        driver.set_page_load_timeout(60)
        driver.get(url)
        wait = WebDriverWait(driver, 100)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tablehead')))
        html = driver.page_source

    except TimeoutException as ex:
        isrunning = 0
        print(str(ex))
        driver.close()
        sys.exit()

    driver.quit()

    soup = BS(html, 'html.parser')
    teamOTable = soup.find_all('table')[0]
    names = ['Rank','Tm', 'Attempts', 'Yds', 'RYds/A', 'Long', 'TD', 'RYds/G', 'Fumbles', 'FumL']
    table = pd.DataFrame(columns=names, index=range(0,32))
    rows = teamOTable.find_all('tr')

    rowMarker = 0
    for i in range(1,len(rows)):
        colMarker = 0
        columns = rows[i].find_all('td')
        for column in columns:
            table.iat[rowMarker, colMarker] = column.get_text()
            colMarker += 1
        rowMarker += 1

    table.sort_values(by=['Tm'], inplace=True)
    table.drop(['Rank','Attempts','Long','Fumbles','FumL'], axis=1, inplace=True)
    table.to_csv(outFileName, index_label=False)

# team receiving @ http://www.espn.com/nfl/statistics/team/_/stat/receiving
# team receiving D @ http://www.espn.com/nfl/statistics/team/_/stat/receiving/position/defense
def scrapeNFLReceivingStats(year=2018, offense=True):
    if offense:
        if year == 2018:
            url = 'http://www.espn.com/nfl/statistics/team/_/stat/receiving'
        else:
            url = 'http://www.espn.com/nfl/statistics/team/_/stat/receiving/year/{}'.format(year)
        outFileName = 'data/nfl/nfl_team_receiving_offense_{}.csv'.format(year)
    else:
        if year == 2018:
            url = 'http://www.espn.com/nfl/statistics/team/_/stat/receiving/position/defense'
        else:
            url = 'http://www.espn.com/nfl/statistics/team/_/stat/receiving/position/defense/year/{}'.format(year)
        outFileName = 'data/nfl/nfl_team_receiving_defense_{}.csv'.format(year)

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(chrome_options=options)

    try:
        driver.set_page_load_timeout(60)
        driver.get(url)
        wait = WebDriverWait(driver, 100)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tablehead')))
        html = driver.page_source

    except TimeoutException as ex:
        isrunning = 0
        print(str(ex))
        driver.close()
        sys.exit()

    driver.quit()

    soup = BS(html, 'html.parser')
    teamOTable = soup.find_all('table')[0]
    names = ['Rank','Tm', 'Receptions', 'ReYds', 'Average', 'Long', 'TD', 'ReYds/G', 'Fumbles', 'FumL']
    table = pd.DataFrame(columns=names, index=range(0,32))
    rows = teamOTable.find_all('tr')

    rowMarker = 0
    for i in range(1,len(rows)):
        colMarker = 0
        columns = rows[i].find_all('td')
        for column in columns:
            table.iat[rowMarker, colMarker] = column.get_text()
            colMarker += 1
        rowMarker += 1

    table.sort_values(by=['Tm'], inplace=True)
    table.drop(['Rank','Receptions','Long','Fumbles','FumL'], axis=1, inplace=True)
    table.to_csv(outFileName, index_label=False)

# schedule @ https://www.pro-football-reference.com/years/{YEAR}/games.htm
def scrapeNFLSchedule(year=2018):

    url = 'https://www.pro-football-reference.com/years/{}/games.htm'.format(year)
    outFileName = 'data/nfl/nfl_games_{}.csv'.format(year)

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(chrome_options=options)

    try:
        driver.set_page_load_timeout(60)
        driver.get(url)
        wait = WebDriverWait(driver, 100)
        wait.until(EC.presence_of_element_located((By.ID, 'games')))
        html = driver.page_source

    except TimeoutException as ex:
        isrunning = 0
        print(str(ex))
        driver.close()
        sys.exit()

    driver.quit()

    soup = BS(html, 'html.parser')
    teamOTable = soup.find_all('table')[0]
    names = ['Day', 'Date', 'Time', 'Winner', '@', 'Loser', 'Box', 'PtsW', 'PtsL', 'YdsW', 'TOW', 'YdsL', 'TOL']
    rows = teamOTable.find_all('tr')
    table = pd.DataFrame(columns=names, index=np.arange(0,len(rows)))

    rowMarker = 0
    for i in range(0,len(rows)):
        colMarker = 0
        columns = rows[i].find_all('td')
        for column in columns:
            table.iat[rowMarker, colMarker] = column.get_text()
            colMarker += 1
        rowMarker += 1

    table.drop(['Day','Date','Time','Box'], axis=1, inplace=True)
    table.dropna(how='all', inplace=True)
    table.to_csv(outFileName, index_label=False)

# team offense @ http://www.espn.com/nba/statistics/team/_/stat/offense-per-game
# team defense @ http://www.espn.com/nba/statistics/team/_/stat/defense-per-game
def scrapeNBATeamStats(offense=True, year=2019):
    if offense:
        if year == 2019:
            url = 'http://www.espn.com/nba/statistics/team/_/stat/offense-per-game'
        else:
            url = 'http://www.espn.com/nba/statistics/team/_/stat/offense-per-game/sort/avgPoints/year/{}'.format(year)
        outFileName = 'data/nba/nba_team_offense_{}.csv'.format(year)
    else:
        if year == 2019:
            url = 'http://www.espn.com/nba/statistics/team/_/stat/defense-per-game'
        else:
            url = 'http://www.espn.com/nba/statistics/team/_/stat/defense-per-game/sort/avgPointsOpponent/year/{}'.format(year)
        outFileName = 'data/nba/nba_team_defense_{}.csv'.format(year)

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(chrome_options=options)

    try:
        driver.set_page_load_timeout(60)
        driver.get(url)
        wait = WebDriverWait(driver, 100)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tablehead')))
        html = driver.page_source

    except TimeoutException as ex:
        isrunning = 0
        print(str(ex))
        driver.close()
        sys.exit()

    driver.quit()

    soup = BS(html, 'html.parser')
    teamOTable = soup.find_all('table')[0]
    names = ['Rank','Tm', 'Points', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%', 'PPS', 'AFG%']
    table = pd.DataFrame(columns=names, index=range(0,30))
    rows = teamOTable.find_all('tr')

    rowMarker = 0
    for i in range(1, len(rows)):
        if i % 11 == 0:
            continue
        colMarker = 0
        columns = rows[i].find_all('td')
        for column in columns:
            table.iat[rowMarker, colMarker] = column.get_text()
            colMarker += 1
        rowMarker += 1

    table.sort_values(by=['Tm'], inplace=True)
    table.drop(['Rank','Points','FGA','FGM','3PA','3PM','FTM'], axis=1, inplace=True)
    table.to_csv(outFileName, index_label=False)

# team rebounds @ http://www.espn.com/nba/statistics/team/_/stat/rebounds-per-game
def scrapeNBATeamReboundStats(year=2019):

    if year == 2019:
        url = 'http://www.espn.com/nba/statistics/team/_/stat/rebounds-per-game'
    else:
        url = 'http://www.espn.com/nba/statistics/team/_/stat/rebounds-per-game/sort/avgRebounds/year/{}'.format(year)

    outFileName = 'data/nba/nba_team_rebounds_{}.csv'.format(year)

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(chrome_options=options)

    try:
        driver.set_page_load_timeout(60)
        driver.get(url)
        wait = WebDriverWait(driver, 100)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tablehead')))
        html = driver.page_source

    except TimeoutException as ex:
        isrunning = 0
        print(str(ex))
        driver.close()
        sys.exit()

    driver.quit()

    soup = BS(html, 'html.parser')
    teamOTable = soup.find_all('table')[0]
    names = ['Rank','Tm', 'OFF%', 'DEF%', 'REB%', 'ORPG', 'OppORPG', 'DRPG', 'OppDRPG', 'RPG', 'OppRPG', 'Diff']
    table = pd.DataFrame(columns=names, index=range(0,30))
    rows = teamOTable.find_all('tr')

    rowMarker = 0
    for i in range(2,len(rows)):
        if i == 13:
            continue
        if i == 25:
            continue
        if i % 12 == 0:
            continue
        colMarker = 0
        columns = rows[i].find_all('td')
        for column in columns:
            table.iat[rowMarker, colMarker] = column.get_text()
            colMarker += 1
        rowMarker += 1

    table.sort_values(by=['Tm'], inplace=True)
    table.drop(['Rank','OFF%','DEF%','REB%'], axis=1, inplace=True)
    table.to_csv(outFileName, index_label=False)

# schedule @ https://www.basketball-reference.com/leagues/NBA_{YEAR}_games-{MONTH}.html
def scrapeNBAScheduleByMonth(year=2019, month='october'):
    url = 'https://www.basketball-reference.com/leagues/NBA_{}_games-{}.html'.format(year,month)
    outFileName = 'data/nba/nba_games_{}_{}.csv'.format(year, month)

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(chrome_options=options)

    try:
        driver.set_page_load_timeout(60)
        driver.get(url)
        wait = WebDriverWait(driver, 100)
        wait.until(EC.presence_of_element_located((By.ID, 'schedule')))
        html = driver.page_source

    except TimeoutException as ex:
        isrunning = 0
        print(str(ex))
        driver.close()
        sys.exit()

    driver.quit()

    soup = BS(html, 'html.parser')
    teamOTable = soup.find_all('table')[0]
    names = ['Start', 'Away', 'AwayPts', 'Home', 'HomePts', 'Boxscore', 'blank', 'Attendance', 'Notes']
    rows = teamOTable.find_all('tr')
    table = pd.DataFrame(columns=names, index=np.arange(0,len(rows)))

    rowMarker = 0
    for i in range(0,len(rows)):
        colMarker = 0
        columns = rows[i].find_all('td')
        for column in columns:
            table.iat[rowMarker, colMarker] = column.get_text()
            colMarker += 1
        rowMarker += 1

    table.drop(['Start','Boxscore','blank','Attendance', 'Notes'], axis=1, inplace=True)
    table.dropna(how='all', inplace=True)
    table.to_csv(outFileName, index_label=False)

def scrapeNBASchedule(years):
    months = ['october', 'november', 'december', 'january', 'february', 'march', 'april']

    for year in years:
        for month in months:
            print("Scraping {}...".format(month))
            scrapeNBAScheduleByMonth(year, month)

def scrapeNBAStatsByYear(years, offense=True):
    for year in years:
        scrapeNBATeamStats(offense, year)
        scrapeNBATeamReboundStats(year)

def scrapeNFLScheduleByYear(years):

    for year in years:
        scrapeNFLSchedule(year)

def scrapeNFLStatsByYear(years, offense=True):
    for year in years:
        scrapeNFLTeamStats(year, offense=True)
        scrapeNFLTeamStats(year, offense=False)
        scrapeNFLPassingStats(year, offense=True)
        scrapeNFLPassingStats(year, offense=False)
        scrapeNFLRushingStats(year, offense=True)
        scrapeNFLRushingStats(year, offense=False)
        scrapeNFLReceivingStats(year, offense=True)
        scrapeNFLReceivingStats(year, offense=False)

# scrape all NFL stats
def scrapeAllNFL():
    scrapeNFLSchedule()
    scrapeNFLTeamStats(offense=True)
    scrapeNFLTeamStats(offense=False)
    scrapeNFLPassingStats(offense=True)
    scrapeNFLPassingStats(offense=False)
    scrapeNFLRushingStats(offense=True)
    scrapeNFLRushingStats(offense=False)
    scrapeNFLReceivingStats(offense=True)
    scrapeNFLReceivingStats(offense=False)

# scrape all NBA stats
def scrapeAllNBA():
    scrapeNBATeamStats(offense=True)
    scrapeNBATeamStats(offense=False)
    scrapeNBATeamReboundStats()

# scrape NFL betting lines
# lines @ https://www.oddsportal.com/american-football/usa/nfl/
def scrapeNFLBetting(week):

    url = 'https://www.oddsportal.com/american-football/usa/nfl/'
    outFileName = 'data/nfl/betting/nfl_bets_week{}.csv'.format(week)

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(chrome_options=options)

    try:
        driver.set_page_load_timeout(60)
        driver.get(url)
        wait = WebDriverWait(driver, 100)
        wait.until(EC.presence_of_element_located((By.ID, 'tournamentTable')))
        html = driver.page_source

    except TimeoutException as ex:
        isrunning = 0
        print(str(ex))
        driver.close()
        sys.exit()

    driver.quit()

    soup = BS(html, 'html.parser')
    teamOTable = soup.find_all('table')[0]
    names = ['Time','Teams','Team1','Team2','B']
    table = pd.DataFrame(columns=names, index=range(0,16))
    rows = teamOTable.find_all('tr')

    rowMarker = 0
    for i in range(3,len(rows)):
        colMarker = 0
        columns = rows[i].find_all('td')
        if len(columns) == 0:
            continue
        if len(columns) > 5:
            continue
        for column in columns:
            table.iat[rowMarker, colMarker] = column.get_text()
            colMarker += 1
        rowMarker += 1

    table.drop(['Time','B'], axis=1, inplace=True)
    table.to_csv(outFileName, index_label=False)
