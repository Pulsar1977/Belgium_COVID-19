#!/usr/bin/env python3
from argparse import ArgumentParser
from configparser import ConfigParser, ExtendedInterpolation
import datetime
import pandas as pd


default_settings = 'covid_Belgium_total_2010-2019.ini'
colors = ['#E6E6FA', '#B0E0E6', '#87CEFA', '#00BFFF', '#1E90FF', '#4682B4', '#0000FF',
          '#00008B', '#7B68EE', '#8A2BE2', '#483D8B']


def init_settings():
    def parser():
        parser = ArgumentParser()
        parser.add_argument('-i', '--input', nargs=1, metavar='file', default=default_settings)
        return parser.parse_args()

    def get_config(configfile):
        config = ConfigParser(interpolation=ExtendedInterpolation())
        config.read(configfile)
        return config

    class Settings:
        def __init__(self, config):
            for key, val in config.items():
                setattr(self, key, val)
            self.extract = self.parse_extract()
            self.prev_years = self.parse_prev_years()
            self.prev_years_str = [str(year) for year in self.prev_years]
            self.all_years = self.prev_years + [2020]

        def parse_extract(self):
            extract = (s.strip() for s in self.extract.split(','))
            return [s for s in extract if s != '']

        def parse_prev_years(self):
            years = []
            for year_str in self.prev_years.split(','):
                start, _, end = year_str.partition('-')
                if end == '':
                    years.append(int(start))
                else:
                    years.extend(range(int(start), int(end)+1))
            return years


    args = parser()
    config = get_config(args.input)
    return Settings(config['Settings'])


def read_data(csvfile, sep=',', parse_dates=['Date']):
    return pd.read_csv(csvfile, sep=sep, infer_datetime_format=True, dayfirst=True,
                       parse_dates=parse_dates)


def store_data(df, csvfile):
    df.to_csv(csvfile, index=False)


def date_to_daynum(date):
    return datetime.date(2020, date.month, date.day).timetuple().tm_yday


def month_day_str_to_daynum(month_day_str):
    d = datetime.datetime.strptime(f'{month_day_str} 2020', '%b %d %Y')
    return d.timetuple().tm_yday


def daynum_to_month_day_str(daynum):
    d = datetime.date(2020, 1, 1) + datetime.timedelta(days=daynum-1)
    return d.strftime('%b %d').replace(" 0", " ")


def month_day_to_month_day_str(month, day):
    return datetime.date(2020, month, day).strftime('%b %d').replace(" 0", " ")
