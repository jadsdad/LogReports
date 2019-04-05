#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import logtools_common.logtools_common as common
import matplotlib.pylab as plt
import os
from matplotlib.backends.backend_pdf import PdfPages

def run():
    with PdfPages(os.path.join(common.basedir, 'Albums by Year of Release.pdf')) as pp:
        sql = "SELECT album.yearreleased as `Year of Release`, count(albumid) as Albums, sum(played) as Played, " \
              "sum(playcount) as Plays FROM albumview as album " \
              "group by album.yearreleased order by album.yearreleased;"
        data = pd.read_sql(sql, common.conn, index_col='Year of Release')
        fig, ax = plt.subplots(figsize=(20, 15))
        data[['Albums', 'Played']].plot(kind='line', ax=ax, title='Albums by Year of Release')
        ax.grid(True, which='major', axis='both')
        pp.savefig(fig)
        plt.close()

        fig, ax = plt.subplots(figsize=(20, 15))
        data['Ratio'] = data['Plays'] / data['Played']
        data['Ratio'].plot(kind='line', ax=ax, title='Plays-per-Album Ratio')
        ax.grid(True, which='major', axis='both')
        pp.savefig(fig)
        plt.close()


if __name__ == '__main__':
    run()