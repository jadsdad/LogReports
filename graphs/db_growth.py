import pandas as pd
import logtools_common.logtools_common as common
import matplotlib.pylab as plt
import os
from datetime import date, timedelta

def run():
    fig, ax = plt.subplots(figsize=(15, 7))

    thresh_date = date.today() - timedelta(weeks=13)
    td_string = thresh_date.strftime("%Y-%m-%d")
    date_range = pd.date_range(td_string, date.today())

    sql = "select cast(album.dateadded as date) as `Date`, count(album.albumid) as `Albums Added` from album where album.albumtypeid <> 16 group by cast(album.dateadded as date);"

    data = pd.read_sql(sql, common.conn, index_col='Date')
    data = data.reindex(date_range, fill_value=0)

    unique_sql = "select log.albumid, min(log.logdate) as first_play from log inner join album on album.albumid = log.albumid where album.albumtypeid <> 16 group by log.albumid asc;"
    unique_data = pd.read_sql(unique_sql, common.conn)
    unique_data = unique_data.groupby('first_play').count()
    unique_data = unique_data.reindex(date_range, fill_value=0)

    data['Albums Played'] = unique_data['albumid']
    data['Progress'] = data['Albums Played'] - data['Albums Added']

    per = data.index.to_period("W")
    results = data.groupby([per]).sum()

    results[['Albums Added', 'Albums Played']].plot(ax=ax, kind='bar', title='DB Growth Rate', legend=True)
    ax.grid(True, which='major', axis='both')
    plt.tight_layout()
    plt.savefig(os.path.join(common.basedir, 'DB Growth rate.pdf'))
    plt.close()

    fig, ax = plt.subplots(figsize=(15, 7))
    results['Progress'].plot(kind='bar', ax=ax, title='Progress', legend=True)
    ax.grid(True, which='major', axis='both')
    plt.axhline(0, color='r')
    plt.tight_layout()
    plt.savefig(os.path.join(common.basedir, 'DB Progress.pdf'))
    #results.to_csv("h:\\data.csv")
    plt.close()


if __name__ == '__main__':
    run()