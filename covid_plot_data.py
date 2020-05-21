#!/usr/bin/env python3
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from covid_init import (init_settings, read_data, store_data, date_to_daynum,
                        month_day_str_to_daynum, daynum_to_month_day_str,
                        month_day_to_month_day_str)


def main(settings):
    plot_settings = PlotSettings(settings)
    data = Data(settings)
    with plt.style.context('bmh'):
        plot_all(plot_settings, data)


class PlotSettings:
    _colors = ['#E6E6FA', '#B0E0E6', '#87CEFA', '#00BFFF', '#1E90FF',
               '#4682B4', '#0000FF', '#00008B', '#7B68EE', '#8A2BE2', '#483D8B']
    _xlabels = [month_day_to_month_day_str(month, 1) for month in range(1, 13)]
    _xticks = [month_day_str_to_daynum(label) for label in _xlabels]

    def __init__(self, settings):
        self.settings = settings
        self.colors = self._colors[-len(settings.prev_years):]
        self.thick = 3
        self.thin = 1.8

    def labels_and_ticks(self, xmin, xmax):
        xticks, xlabels = zip(*[(xtick, xlabel) for (xtick, xlabel)
                                in zip(self._xticks, self._xlabels) if xmin <= xtick <= xmax])
        return xticks, xlabels


class Data:
    def __init__(self, settings):
        self.all_2020_df = read_data(settings.alldeaths_2020_csv, parse_dates=[])
        self.all_prev_df = read_data(settings.alldeaths_prev_years_csv, parse_dates=[])
        self.cov_2020_df = read_data(settings.covdeaths_2020_csv, parse_dates=[])
        for df in (self.all_2020_df, self.all_prev_df, self.cov_2020_df):
            df.set_index('Daynum', inplace=True)
        self.set_interpolate(settings)

    def set_interpolate(self, settings):
        self.all_prev = {}
        self.all_2020 = {}
        df1 = self.all_prev_df
        for key in settings.prev_years_str + ['Mean', 'Std']:
            self.all_prev[key] = interp1d(df1.index.to_list(), df1[key].to_list(), kind='cubic')
        df2 = self.all_2020_df
        for key in ['Deaths', 'Excess', 'Cumexcess']:
            self.all_2020[key] = interp1d(df2.index.to_list(), df2[key].to_list(), kind='cubic')
        self.cov_2020 = df3 = self.cov_2020_df
        x = self.xnonlist()
        df_diff = df2.loc[x[0]:x[-1], 'Deaths'] - df3.loc[x[0]:x[-1], 'Deaths']
        df_diff_cum = df2.loc[x[0]:x[-1], 'Excess'] - df3.loc[x[0]:x[-1], 'Deaths']
        self.non_2020 = interp1d(x, df_diff.to_list(), kind='cubic')
        self.non_cum_2020 = interp1d(x, df_diff_cum.to_list(), kind='cubic')

    def xprev(self, xmin, xmax, num=500):
        return np.linspace(xmin, xmax, num, endpoint=True)

    def x2020(self, xmin, xmax, num=500):
        xmin = max(xmin, self.all_2020_df.index[0])
        xmax = min(xmax, self.all_2020_df.index[-1])
        return np.linspace(xmin, xmax, num, endpoint=True)

    def xnonlist(self):
        xmin = self.cov_2020_df.index[0]
        xmax = self.all_2020_df.index[-1]
        return list(range(xmin, xmax+1))

    def xnon(self, xmin, xmax, num=500):
        xmin = max(xmin, self.cov_2020_df.index[0])
        xmax = min(xmax, self.all_2020_df.index[-1])
        return np.linspace(xmin, xmax, num, endpoint=True)

    def xcov(self, xmin, xmax):
        xmin = max(xmin, self.cov_2020_df.index[0])
        xmax = min(xmax, self.cov_2020_df.index[-1])
        return list(range(xmin, xmax+1))


def plot_all(plot_settings, data):
    plt.rc('font', family='serif', weight=500, size=16)
    plt.rc('legend', handlelength=1.4, fontsize=15)
    plt.rc('axes', labelweight=500)
    plt.rc('figure', titleweight='bold', titlesize=26)
    fig, ax = plt.subplots(3, 1, figsize=(10,14), dpi=150)
    fig.tight_layout(rect=[0.005, -0.005, 1, 0.96])
    plt.suptitle('Belgium: daily deaths 2010-2020', y=0.98)

    xmin, xmax = month_day_str_to_daynum('Jan 24'), month_day_str_to_daynum('May 8')
    ax11, ax12 = plot1(plot_settings, data, ax[0], xmin, xmax, ymin=0, ymax=700)
    ax21, ax22 = plot2(plot_settings, data, ax[1], xmin, xmax, ymin=-100, ymax=400)
    ax31, ax32 = plot3(plot_settings, data, ax[2], xmin, xmax, ymin=-400, ymax=9000)

    plt.savefig('Belgium_total_2010-2020.png', dpi=150, format='png')
    plt.savefig('Belgium_total_2010-2020.pdf', dpi=150, format='pdf')
    plt.savefig('Belgium_total_2010-2020.svg', dpi=150, format='svg')


def plot1(plot_settings, data, ax1, xmin, xmax, ymin, ymax):
    prev_years_str = plot_settings.settings.prev_years_str
    thick, thin = plot_settings.thick, plot_settings.thin
    ax1, ax2 = set_axes(plot_settings, ax1, xmin, xmax, ymin, ymax, mxticks=1, myticks=20)
    xprev = data.xprev(xmin, xmax, num=500)
    x2020 = data.x2020(xmin, xmax, num=500)
    xnon = data.xnon(xmin, xmax, num=500)
    ymean = data.all_prev['Mean'](xprev)
    ystd = data.all_prev['Std'](xprev)
    ynon = data.non_2020(xnon)
    ax1.fill_between(xprev, ymean-ystd, ymean+ystd, color='darkslategray', alpha=0.4)
    ax1.fill_between(xprev, ymean-2*ystd, ymean+2*ystd, color='darkslategray', alpha=0.15)
    for year, color in zip(prev_years_str, plot_settings.colors):
        ax1.plot(xprev, data.all_prev[year](xprev), color=color, lw=thin, label=year, zorder=2.5)
    ax1.plot(xprev, ymean, color='black', lw=thick, label='2010-2019 mean', zorder=2.5)
    ax1.plot(x2020, data.all_2020['Deaths'](x2020), color='red', lw=thick, label='2020 (all)', zorder=3)
    ax1.plot(xnon, ynon, color=(1,100/255,0), lw=2.5, zorder=2.5, label='2020 (non-COVID)')
    ax1.legend(loc='upper left', ncol=3, handlelength=1.4, labelspacing=0.12,
               columnspacing=1.2, fontsize=14)    
    return ax1, ax2


def plot2(plot_settings, data, ax1, xmin, xmax, ymin, ymax):
    thick, thin = plot_settings.thick, plot_settings.thin
    first_case = month_day_str_to_daynum('Mar 10')
    ax1, ax2 = set_axes(plot_settings, ax1, xmin, xmax, ymin, ymax, mxticks=1, myticks=20)
    x2020 = data.x2020(xmin, xmax, num=500)
    xnon = data.xnon(xmin, xmax, num=500)
    ynon_cum = data.non_cum_2020(xnon)
    xcov = data.xcov(xmin, xmax-1)
    ycov = data.cov_2020.loc[xcov[0]:xcov[-1], 'Deaths'].to_list()
    ax1.bar(xcov, ycov, color='darkgoldenrod', zorder=2.5,
            label='Reported COVID-19 deaths')
    ax1.annotate("First Death", xy=(first_case, 15), xycoords='data', xytext=(first_case, 100),
                 ha='center', va='bottom', color='darkgoldenrod', weight=600, zorder=2,
                 arrowprops=dict(width=3.5, headwidth=10, shrink=3, facecolor='darkgoldenrod'))
    ax1.axhline(0, color="black", lw=thick, zorder=2.5)
    ax1.plot(x2020, data.all_2020['Excess'](x2020), color='red', lw=thick, zorder=3,
             label='All excess deaths 2020 w.r.t. 2010-2019 mean')
    ax1.plot(xnon, ynon_cum, color=(1,100/255,0), lw=2.5, zorder=2.5,
             label='Non-COVID excess deaths 2020')
    ax1.legend(loc='upper left')
    return ax1, ax2


def plot3(plot_settings, data, ax1, xmin, xmax, ymin, ymax):
    thick, thin = plot_settings.thick, plot_settings.thin
    first_case = month_day_str_to_daynum('Mar 10')
    ax1, ax2 = set_axes(plot_settings, ax1, xmin, xmax, ymin, ymax, mxticks=1, myticks=100)
    xcum = data.x2020(first_case, xmax, num=500)
    xcov = data.xcov(xmin, xmax-1)
    ycov = data.cov_2020.loc[xcov[0]:xcov[-1], 'Cumdeaths'].to_list()
    ax1.bar(xcov, ycov, color='darkgoldenrod', zorder=3,
            label='Cumulative reported COVID-19 deaths')
    ax1.annotate("First Death", xy=(first_case, 100), xycoords='data', xytext=(first_case, 2000),
                 ha='center', va='top', color='darkgoldenrod', weight=600, zorder=2,
                 arrowprops=dict(width=3.5, headwidth=10, shrink=3, facecolor='darkgoldenrod'))
    ax1.axhline(0, color="black", lw=thick, zorder=3)
    cuminit = data.all_2020['Cumexcess'](xcum[0])
    ax1.plot(xcum, data.all_2020['Cumexcess'](xcum) - cuminit + 1, color='red',
             lw=thick, zorder=3, label='Cumulative excess deaths since Mar 10, 2020')
    ax1.legend(loc='upper left')
    return ax1, ax2


def set_axes(plot_settings, ax1, xmin, xmax, ymin, ymax, mxticks, myticks):
    ax1.set_xlim(xmin, xmax)
    ax1.set_ylim(ymin, ymax)
    ax1.xaxis.set_minor_locator(MultipleLocator(mxticks))
    ax1.yaxis.set_minor_locator(MultipleLocator(myticks))
    xticks, xlabels = plot_settings.labels_and_ticks(xmin, xmax)
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(xlabels)
    ax2 = ax1.twinx()
    ax2.set_ylim(ax1.get_ylim())
    ax2.yaxis.set_minor_locator(MultipleLocator(myticks))
    ax2.set_yticklabels([])
    ax2.set_zorder(-1)
    ax1.patch.set_visible(False)
    ax2.patch.set_visible(True)
    return ax1, ax2


if __name__ == "__main__":
    settings = init_settings()
    main(settings)
