from string import ascii_lowercase
import requests
from bs4 import BeautifulSoup
import pandas
import os
import csv

def scrape(start_year, end_year, file_path=os.getcwd()):
    for letter in ascii_lowercase:
        player_list = BeautifulSoup(requests.get("{}{}/".format(base_url, letter)).content, 'html.parser')
        for player in player_list.find("div", {"id": "div_players_"}).find_all("p"):
            years = player.text[player.text.find("(") + 1:len(player.text) - 1]
            first_year, last_year = years.split("-")
            if int(last_year) > start_year:
                player_id_url = player.find("a")
                player_name = player_id_url.text
                player_id = player_id_url['href'][player_id_url['href'].rfind("/") + 1:player_id_url['href'].rfind(".")]
                iter_year_start, iter_year_end = max(start_year, int(first_year)), min(end_year, int(last_year))
                print(player_name)
                for year in range(iter_year_start, iter_year_end + 1):
                    print(year)
                    log_url = "{}id={}&t=p&year={}".format(pitching_log_url, player_id, year)
                    try:
                        table = pandas.read_html(log_url)[0]
                    except ValueError:
                        continue
                    table = table[table.Opp != "Opp"]
                    table = table[:-1]
                    table.to_csv(os.path.join(file_path, "{} {} Pitching Logs.csv".format(player_name, year)))


base_url = "https://www.baseball-reference.com/players/"
pitching_log_url = "https://www.baseball-reference.com/players/gl.fcgi?"