#!/usr/bin/env python3
import pandas as pd
from covid_init import init_settings, read_data, store_data, date_to_daynum


def main(settings):
    extract_alldeaths_data(settings)
    extract_covdeaths_data(settings)


def extract_alldeaths_data(settings):
    extract, prev_years_str = settings.extract, settings.prev_years_str
    df = read_data(settings.alldeaths_cleaned_csv)
    df = group_data(df, extract)
    df_2020, df_prev_years = extract_years(df, extract, prev_years_str)
    df_prev_years = finish_df_prev_years(df_prev_years, extract, prev_years_str)
    df_2020 = finish_df_2020(df_2020, df_prev_years, extract)
    store_data(df_2020, settings.alldeaths_2020_csv)
    store_data(df_prev_years, settings.alldeaths_prev_years_csv)


def extract_covdeaths_data(settings):
    df = read_data(settings.covdeaths_cleaned_csv)
    df = group_data(df, settings.extract)
    store_data(df, settings.covdeaths_2020_csv)


def group_data(df, extract):
    df.dropna(how='any', subset=extract)
    group_columns = extract + ['Year', 'Date']
    df.sort_values(by=group_columns, inplace=True)
    df = df.groupby(group_columns)['Deaths'].sum().reset_index()
    df['Cumdeaths'] = df.groupby(extract + ['Year'])['Deaths'].cumsum()
    df['Daynum'] = df['Date'].apply(date_to_daynum)
    df.drop(columns=['Date'], inplace=True)
    return df


def extract_years(df, extract, prev_years_str):
    df_2020 = df.loc[df['Year'] == 2020].copy()
    df.set_index(['Daynum'] + extract, inplace=True)
    dfs = [df.loc[df['Year'] == int(year), ['Deaths']].rename(columns={'Deaths': year})
           for year in prev_years_str]
    df_prev_years = pd.concat(dfs, axis=1)
    df_prev_years.reset_index(inplace=True)
    return df_2020, df_prev_years


def finish_df_prev_years(df_prev_years, extract, prev_years_str):
    frame = df_prev_years if extract == [] else df_prev_years.grouby(extract)
    df_prev_years[prev_years_str] = frame[prev_years_str].interpolate(method='cubic')
    df_prev_years[['Mean', 'Std']] = df_prev_years[prev_years_str].agg(['mean', 'std'], axis=1)
    return df_prev_years


def finish_df_2020(df_2020, df_prev_years, extract):
    df_2020.set_index(['Daynum'] + extract, inplace=True)
    df_prev_years.set_index(['Daynum'] + extract, inplace=True)
    last_ind = df_2020.index[-1]
    df_2020['Excess'] = df_2020['Deaths'] - df_prev_years.loc[:last_ind, 'Mean']
    df_2020.reset_index(inplace=True)
    df_prev_years.reset_index(inplace=True)
    frame = df_2020 if extract == [] else df_2020.grouby(extract)
    df_2020['Cumexcess'] = frame['Excess'].cumsum()
    return df_2020


if __name__ == '__main__':
    settings = init_settings()
    main(settings)
