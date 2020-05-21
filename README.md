# Belgium: Daily Deaths 2010-2019 vs COVID-19 Deaths

Belgium has been hit very hard by COVID-19. In particular, the death toll per capita (78 per 100,000) seems exceptionally high, 
which has raised some eyebrows internationally. The main reason for this high number, compared to neighbouring countries, is
the fact that Belgium chooses to include unconfirmed cases in their daily reports, that is, people who died with 
COVID-19 symptoms but weren't tested. Less than 60% of the reported deaths to date (May 21) were tested.

To show that this extensive reporting is justified, I decided to plot the reported COVID-19 deaths against the total excess
mortality of 2020. This is calculated as the relative daily number of deaths in 2020 above or below the average dailty number
of deaths of the past 10 years. The data are pulled from 
[Statbel](https://statbel.fgov.be/en/open-data/number-deaths-day-sex-district-age)
and
[Sciensano/Epistat](https://epistat.wiv-isp.be/covid/) (mortality by date, age, sex, and region).

Every country uses different criteria in their reporting, so to understand the true impact of COVID-19 it is important to
obtain an objective measure. The excess deaths provide the most accurate estimate of real death toll due to COVID-19. 
These graphs show that overall, the reported cases in Belgium do track the excess deaths very well.

The first graph shows all daily deaths between 2010 and 2020, provided by Statbel, the Belgian Institute for Statistics. 
The black line is the 2010-2019 mean, which I will use as the baseline for the second and third graph; 
the grey areas are the 1σ and 2σ standard deviations. The red line shows all 2020 deaths. 
From this, the reported COVID-19 deaths are subtracted to obtain the non-COVID deaths (orange line). 
Clearly, the impact of COVID-19 is huge.

The second graph shows the 2020 excess deaths, that is, the 2020 deaths minus the 2010-2019 mean. 
The bar graph shows the reported COVID-19 deaths.

The third graphs shows the cumulative excess deaths and COVID-19 deaths since Mar 10, 2020 
(the date of the first reported COVID-19 death).

It seems that in the early weeks of the outbreak, there might have been a slight under-reporting. 
This wouldn't be surprising, as COVID-19 symptoms in casualties outside hospitals were probably unnoticed or 
erroneously attributed to other causes like flu.

Conversely, in recent weeks the reported COVID-19 death toll is higher than the excess death. This could be a sign of the
so-called [harvesting effect](https://en.wikipedia.org/wiki/Mortality_displacement), i.e. a subsequent reduction in mortality
because COVID-19 has killed elderly people with comorbitities who would've died in the short-term anyway. 
There may also be indirect consequences of the lockdown. 
Still, note that the excess death before the outbreak was below the 2010-2019 mean (due to a mild flu season), 
and the recent non-COVID excess deaths are in line with the situation before the outbreak. 
Also, it's important to keep in mind that the national overall stats are provisional and possibly still incomplete, 
in particular the most recent data.

---

#### Usage

- `covid_download_data.py`: download the latest data. By default, the daily COVID-19 data from Sciensano are downloaded. 
With the flag `-a`, the weekly total death stats from Statbel are downloaded as well (updated every Friday). Note that these latter files have a 
different name each week.

- `covid_cleanup_data.py`: write the data into standardized `csv` files.

- `covid_extract_data.py`: group and extract specific data, based on input from a config file (by default, 
`covid_Belgium_total_2010-2019.ini`) The config variable `extract` allows to group the data further into smaller subsets like
Sex, Region, and AgeGroup. Default: ''. The config variable `prev_years` selects the years to calculate the expected daily 
deaths, to be used as the baseline for the 2020 excess deaths. Default: '2010-2019'.

- `covid_plot_data.py`: plot the data. Output in `pdf`, `png`, `jpg`, or `svg`.

---

#### Requirements

Python 3.6+, pandas, numpy, matplotlib.
