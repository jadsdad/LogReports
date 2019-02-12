#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import logtools_common.logtools_common as common
import matplotlib.pylab as plt
import os

from matplotlib.backends.backend_pdf import PdfPages

def run():
    sql = "SELECT log.logDate, source.Source as Source, count(log.logID) as Plays " \
          "FROM log INNER JOIN album ON log.AlbumID = album.AlbumID " \
          "inner join source on album.SourceID = source.sourceid " \
          "WHERE album.SourceID <> 6 and log.logDate >= '2018-01-01'" \
          "GROUP BY log.logdate, Source ORDER BY logdate, Source;"

    with PdfPages(os.path.join(common.basedir, 'Media Summary Graphs.pdf')) as pp:
        results = pd.read_sql(sql, common.conn)
        results['logDate'] = pd.to_datetime(results['logDate'])
        per = results['logDate'].dt.to_period("M")
        results = results.groupby([per,'Source'])
        graph_results = results.sum()
        fig, ax = plt.subplots(figsize=(15,7))
        graph_results = graph_results['Plays'].unstack().fillna(0)
        graph_results.plot(ax=ax, title="Media Summary")
        ax.grid(True, which='major', axis='both')
        ax.grid(True, which='minor', axis='x')

        pp.savefig(fig)
        plt.close()

if __name__ == '__main__':
    run()

