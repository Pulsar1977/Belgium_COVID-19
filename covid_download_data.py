#!/usr/bin/env python3
import argparse
from downloader import download, unzip

alldeaths_url = 'https://statbel.fgov.be/sites/default/files/files/opendata/deathday/DEMO_DEATH_OPEN.zip'
alldeaths_zip = 'DEMO_DEATH_OPEN.zip'
covdeaths_url = 'https://epistat.sciensano.be/Data/COVID19BE_MORT.csv'


def main():
    args = argparser()
    print(f'Downloading {covdeaths_url}...')
    download(covdeaths_url)
    if args.download_all:
        print(f'Downloading {alldeaths_url}...')
        download(alldeaths_url)
        unzip(alldeaths_zip)


def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--download_all', action='store_true')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
