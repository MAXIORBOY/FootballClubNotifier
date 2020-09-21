import tkinter as tk
from tkinter import ttk, font, messagebox
import json
import os
import requests
import re
import bs4 as bs
import sys
import math as mth


class Config:
    def __init__(self):
        self.club_names = []
        self.league_name = ''
        self.league_url_parts_dictionary = self.set_league_url_parts_dictionary()

    @staticmethod
    def window_position_adjuster(window, width_adjuster=0.7, height_adjuster=0.7):
        window.update()
        window.geometry('%dx%d+%d+%d' % (window.winfo_width(), window.winfo_height(), width_adjuster * ((window.winfo_screenwidth() - window.winfo_width()) / 2), height_adjuster * ((window.winfo_screenheight() - window.winfo_height()) / 2)))

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
                "Veikkausliiga (FIN)": 'finnish-veikkausliiga'}

    def set_league_name(self, league_name):
        self.league_name = league_name

    def get_current_club_names_from_league(self):
        self.club_names = []
        response = requests.get('https://www.bbc.com/sport/football/' + self.league_url_parts_dictionary[self.league_name] + '/table').content
        soup = bs.BeautifulSoup(response, 'lxml')
        table_rows = (soup.find('tbody')).findAll('abbr', attrs={'class': "sp-u-abbr-on sp-u-abbr-off@m"})
        for row in table_rows:
            club_name = re.search('title="(.*)">', str(row)).group(1)
            self.club_names.append(club_name[:club_name.find('"')])

        self.club_names = sorted(self.club_names)

    def start_config(self):
        window = tk.Tk()
        window.title('Config')

        tk.Label(window, text='Football Club Notifier - Configuration:\n', bd=4, font=font.Font(family='Helvetica', size=13, weight='bold')).pack()
        tk.Label(window, text='Select the league:\n', bd=4, font=font.Font(family='Helvetica', size=11, weight='bold')).pack()
        league_name = tk.StringVar()
        combo_box = ttk.Combobox(window, width=30, textvariable=league_name)
        combo_box['values'] = list(self.league_url_parts_dictionary.keys())
        combo_box.pack()

        tk.Label(window, text='').pack()
        button = tk.Button(window, text='NEXT', bd=4, font=10, command=lambda: [window.destroy(), self.set_league_name(league_name.get()), self.pick_club()])
        button.pack()

        self.window_position_adjuster(window)
        window.mainloop()

    def save_favourite_club_name(self, club_name):
        with open(os.path.join(os.environ['APPDATA'], 'FCN_club_info.json'), 'w', encoding="utf8") as f:
            json.dump([club_name, self.league_name], f)

    def pick_club(self):
        window = tk.Tk()
        window.title('Config')

        tk.Label(window, text='Select the club:\n', bd=4, font=font.Font(family='Helvetica', size=12, weight='bold')).pack()

        try:
            self.get_current_club_names_from_league()
        except:
            window.withdraw()
            m_box = messagebox.showerror("Error", 'Connection to the website has failed. Please try again later.')
            if m_box == 'ok':
                window.destroy()
                sys.exit()

        radio_button_var = tk.IntVar()

        big_frame = tk.Frame(window)
        frame_left = tk.Frame(big_frame)
        for i in range(mth.ceil(len(self.club_names) / 2)):
            tk.Radiobutton(frame_left, text=self.club_names[i], value=i, variable=radio_button_var, font=font.Font(family='Helvetica', size=12, weight='normal')).pack()

        frame_right = tk.Frame(big_frame)
        for i in range(mth.ceil(len(self.club_names) / 2), len(self.club_names)):
            tk.Radiobutton(frame_right, text=self.club_names[i], value=i, variable=radio_button_var, font=font.Font(family='Helvetica', size=12, weight='normal')).pack()

        frame_left.pack(side=tk.LEFT)
        frame_right.pack(side=tk.LEFT)
        big_frame.pack()

        tk.Label(window, text='').pack()
        tk.Button(window, text='FINISH', bd=4, font=10, command=lambda: [self.save_favourite_club_name(self.club_names[radio_button_var.get()]), window.destroy()]).pack()
        tk.Button(window, text='BACK', bd=4, font=10, command=lambda: [window.destroy(), self.start_config()]).pack()

        self.window_position_adjuster(window)
        window.mainloop()


if __name__ == '__main__':
    Config().start_config()
