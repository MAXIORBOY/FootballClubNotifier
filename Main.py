import requests
import re
import time
import sys
import datetime as dt
import bs4 as bs
import plyer as pl
import json
import os
import tkinter as tk
from tkinter import messagebox
import pytz


class Match:
    def __init__(self, teams, match_date, league_type):
        self.team1 = teams[0]
        self.team2 = teams[1]
        self.match_date = match_date
        self.league_type = league_type


class FootballClubNotifier:
    def __init__(self, actual_date, notification_duration=15):
        self.month_dictionary = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
        self.notification_duration = notification_duration
        self.actual_date = actual_date
        self.london_time = dt.datetime.now(tz=pytz.timezone('Europe/London'))
        self.offset = dt.timedelta(hours=self.actual_date.hour, minutes=self.actual_date.minute) - dt.timedelta(hours=self.london_time.hour, minutes=self.london_time.minute)
        self.favourite_club_name, self.club_home_league_name = self.load_data_from_file()
        self.league_types = [self.club_home_league_name, 'Champions League', 'Europa League']
        self.league_url_part_dictionary = self.set_league_url_parts_dictionary()
        self.responses = [self.get_league_response(self.league_url_part_dictionary[self.club_home_league_name]), self.get_league_response(self.league_url_part_dictionary["Champions League"]), self.get_league_response(self.league_url_part_dictionary["Europa League"])]
        self.results = None

    @staticmethod
    def load_data_from_file():
        try:
            return json.load(open(os.path.join(os.environ['APPDATA'], 'FCN_club_info.json'), 'r'))
        except:
            root = tk.Tk()
            root.withdraw()
            m_box = messagebox.showerror("Error", 'Configuration file does not exist or is corrupted. Please create a new one via FCN_config.exe program.')
            if m_box == 'ok':
                sys.exit()

    @staticmethod
    def set_league_url_parts_dictionary():
        return {"Allsvenskan (SWE)": 'swedish-allsvenskan',
                "Bundesliga (AUS)": 'austrian-bundesliga',
                "Bundesliga (GER)": 'german-bundesliga',
                "Eliteserien (NOR)": 'norwegian-tippeligaen',
                "Eredivisie (NED)": 'dutch-eredivisie',
                "First Division A (BEL)": 'belgian-pro-league',
                "La Liga (SPA)": 'spanish-la-liga',
                "Ligue 1 (FRA)": 'french-ligue-one',
                "Premier Division (IRE)": 'league-of-ireland-premier',
                "Premier League (ENG)": 'premier-league',
                "Premier League (RUS)": 'russian-premier-league',
                "Premiership (SCO)": 'scottish-premiership',
                "Primeira Liga (POR)": 'portuguese-primeira-liga',
                "Serie A (ITA)": 'italian-serie-a',
                "Super League (SWI)": 'swiss-super-league',
                "Super Lig (TUR)": 'turkish-super-lig',
                "Superleague (GRE)": 'greek-superleague',
                "Superliga (DEN)": 'danish-superliga',
                "Veikkausliiga (FIN)": 'finnish-veikkausliiga',
                "Champions League": 'champions-league',
                "Europa League": 'europa-league'}

    def no_internet_connection_sleep(self):
        time.sleep(300)
        self.actual_date = self.actual_date + dt.timedelta(minutes=5)

    def get_league_response(self, league_string):
        while True:
            try:
                return requests.get('https://www.bbc.com/sport/football/' + league_string + '/scores-fixtures/' + str(self.actual_date.year) + '-' + str(self.actual_date.month).zfill(2)).content
            except:
                self.no_internet_connection_sleep()

    def find_club_matches(self):
        result_tab = []
        for i in range(len(self.responses)):
            soup = bs.BeautifulSoup(self.responses[i], 'lxml')
            all_matches = soup.findAll('div', attrs={'class': "qa-match-block"})

            for matches_in_one_day in all_matches:
                try:
                    match_date = re.search('>(.*)<', str(matches_in_one_day.find('h3', attrs={'class': 'gel-minion sp-c-match-list-heading'}))).group(1)
                    week_day, day, month = match_date.split(' ')
                    day = int(day[:-2])
                    month = self.month_dictionary[month]
                except:
                    day, month = self.actual_date.day, self.actual_date.month

                daily_match = matches_in_one_day.findAll('li', attrs={'class': "gs-o-list-ui__item gs-u-pb-"})
                for match in daily_match:
                    hour, minutes = -1, -1
                    try:
                        match_did_not_start_flag = True
                        match_clock = re.search('>(.*)<', str(match.find('span', attrs={"class": "sp-c-fixture__number sp-c-fixture__number--time"}))).group(1)
                        hour, minutes = match_clock.split(':')
                        hour = int(hour)
                        minutes = int(minutes)
                    except:
                        match_did_not_start_flag = False

                    teams = match.findAll('span', attrs={'class': "gs-u-display-none gs-u-display-block@m qa-full-team-name sp-c-fixture__team-name-trunc"})
                    teams_names = []
                    for team in teams:
                        teams_names.append(re.search('>(.*)<', str(team)).group(1))

                    if self.favourite_club_name in teams_names and match_did_not_start_flag:
                        full_date = dt.datetime(year=self.actual_date.year, month=month, day=day, hour=hour, minute=minutes) + self.offset
                        result_tab.append(Match(teams_names, full_date, self.league_types[i]))

        return result_tab

    def send_notification(self, index, state):
        def build_notification_string():
            return self.results[index].league_type + '\n' + self.results[index].team1 + ' vs ' + self.results[index].team2 + '\n' + self.results[index].match_date.strftime('%H:%M')
        title_dictionary = {0: "Today's Match:", 1: "The match starts in 1 hour!", 2: "The match is about to start!"}
        pl.notification.notify(title='(FCN)  ' + title_dictionary[state], message=build_notification_string(), timeout=self.notification_duration)
        time.sleep(self.notification_duration)

    def start(self):
        self.results = self.find_club_matches()
        index = -1
        seconds = -1
        for i in range(len(self.results)):
            delta = self.results[i].match_date - self.actual_date
            if delta.days == 0:
                index = i
                seconds = delta.seconds
                break

        if index != -1:
            minimal_time = self.results[index].match_date.hour * 3600 + self.results[index].match_date.minute * 60
            while seconds > minimal_time:
                time.sleep(1)
                seconds -= 1

            self.send_notification(index, 0)
            seconds -= self.notification_duration

            while seconds > 3600:
                time.sleep(1)
                seconds -= 1

            if seconds > 3540:
                self.send_notification(index, 1)
                seconds -= self.notification_duration

            while seconds:
                time.sleep(1)
                seconds -= 1

            self.send_notification(index, 2)
            seconds -= self.notification_duration

            sys.exit()
        else:
            sys.exit()


if __name__ == "__main__":
    FootballClubNotifier(dt.datetime.now()).start()
