#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import logtools_common.logtools_common as common
import matplotlib.pylab as plt
import os
from datetime import date
from matplotlib.backends.backend_pdf import PdfPages

def run():
    with PdfPages(os.path.join(common.basedir, 'Catalogue Size.pdf')) as pp:
        sql = "select album.dateadded as `Date`, count(albumid) as `Albums` from albumview as album " \
              "group by dateadded;"
        data = pd.read_sql(sql, common.conn)
        data['Date'] = pd.to_datetime(data['Date'])
        per = data['Date'].dt.to_period("D")
        results = data.groupby([per]).sum().squeeze().cumsum()

        fig, ax = plt.subplots(figsize=(15, 7))
        results.plot(ax=ax, title='Catalogue Size')
        ax.grid(True, which='major', axis='both')
        plt.ylim(bottom=1000)
        plt.xlim(left=date(2019,1,1), right=date.today())
        pp.savefig()
        plt.close()

        sql = "select album.dateadded as `Date`, source.source, count(albumid) as `Albums` " \
              "from albumview as album inner join source on album.sourceid=source.sourceid " \
              "group by dateadded, source;"

        data = pd.read_sql(sql, common.conn)
        data['Date'] = pd.to_datetime(data['Date'])
        per = data['Date'].dt.to_period("D")
        results = data.groupby([per, 'source']).sum()
        results['Cumulative'] = results.groupby('source')['Albums'].transform(pd.Series.cumsum)

        fig, ax = plt.subplots(figsize=(15, 7))
        results['Cumulative'].unstack().fillna(method='ffill').plot(ax=ax, title='Catalogue Size by Media')
        ax.grid(True, which='major', axis='both')
        plt.xlim(left=date(2019,1,1), right=date.today())
        pp.savefig()
        plt.close()

if __name__ == '__main__':
    run()