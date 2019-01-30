#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import logtools_common.logtools_common as common
import matplotlib.pylab as plt
import os

def run():
    sql = "select album.dateadded as `Date`, count(albumid) as `Albums` from album where album.albumtypeid <> 16 group by dateadded;"
    data = pd.read_sql(sql, common.conn)
    data['Date'] = pd.to_datetime(data['Date'])
    per = data['Date'].dt.to_period("D")
    results = data.groupby([per]).sum().squeeze().cumsum()

    fig, ax = plt.subplots(figsize=(15,7))
    results.plot(ax=ax, title='Catalogue Size')
    ax.grid(True, which='major', axis='both')
    plt.savefig(os.path.join(common.basedir, 'Catalogue Size.pdf'))
    plt.close()

if __name__ == '__main__':
    run()