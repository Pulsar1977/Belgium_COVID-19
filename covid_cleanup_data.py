#!/usr/bin/env python3
from covid_init import init_settings, read_data, store_data


def main(settings):
    clean_alldeaths_data(settings)
    clean_covdeaths_data(settings)


def clean_alldeaths_data(settings):
    df = read_data(settings.alldeaths_raw_csv, sep=';', parse_dates=['DT_DATE'])
    df.rename(columns={'CD_ARR': 'Arr', 'CD_PROV': 'Prov', 'CD_REGIO': 'Region',
                       'CD_SEX': 'Sex', 'CD_AGEGROUP': 'AgeGroup', 'DT_DATE': 'Date',
                       'NR_YEAR': 'Year', 'NR_WEEK': 'Week', 'MS_NUM_DEATH': 'Deaths'
                       }, inplace=True)
    df['Sex'] = df['Sex'].replace({1: 'M', 2: 'F'})
    df['Region'] = df['Region'].replace({2000: 'Flanders', 3000: 'Wallonia',
                                         4000: 'Brussels'})
    store_data(df, settings.alldeaths_cleaned_csv)


def clean_covdeaths_data(settings):
    df = read_data(settings.covdeaths_raw_csv, parse_dates=['DATE'])
    df.rename(columns={'DATE': 'Date', 'REGION': 'Region', 'AGEGROUP': 'AgeGroup',
                       'SEX': 'Sex', 'DEATHS': 'Deaths'}, inplace=True)
    df['Year'] = 2020
    store_data(df, settings.covdeaths_cleaned_csv)


if __name__ == '__main__':
    settings = init_settings()
    main(settings)
