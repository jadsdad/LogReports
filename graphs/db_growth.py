import pandas as pd
import logtools_common.logtools_common as common
import matplotlib.pylab as plt
import os

def run():
    fig, ax = plt.subplots(figsize=(15, 7))

    sql = "select CAST(album.dateadded as DATE) as `Date`, count(album.albumid) as `Albums` from album INNER JOIN (select log.albumid, min(log.logdate) as first_play from log group by log.albumid) ESC on ESC.albumid = album.albumid where album.albumtypeid <> 16 and datediff(album.dateadded, ESC.first_play) <= 7 group by dateadded;"

    data = pd.read_sql(sql, common.conn)
    data['Date'] = pd.to_datetime(data['Date'])
    data = data[data['Date'] >= '2018-12-01']
    per = data['Date'].dt.to_period("W")
    results = data.groupby([per]).sum()
    results['Growth'] = results['Albums']

    unique_sql = "select log.albumid as `New Albums Played`, min(log.logdate) as first_play from log inner join album on album.albumid = log.albumid where album.albumtypeid <> 16 group by log.albumid order by logdate asc;"
    unique_data = pd.read_sql(unique_sql, common.conn)
    unique_data['first_play'] = pd.to_datetime(unique_data['first_play'])
    unique_data = unique_data[unique_data['first_play'] >= '2018-12-01']
    unique_per = unique_data['first_play'].dt.to_period("W")
    unique_results = unique_data.groupby([unique_per]).count()

    results['New Albums Played'] = unique_results['New Albums Played']
    results['Progress'] = results['New Albums Played'] - results['Growth']

    results[['Growth', 'New Albums Played']].plot(ax=ax, title='DB Growth Rate', legend=True)

    ax.grid(True, which='major', axis='both')
    plt.savefig(os.path.join(common.basedir, 'DB Growth rate.pdf'))
    plt.close()

    fig, ax = plt.subplots(figsize=(15, 7))
    results['Progress'].plot(kind='bar', ax=ax, title='Progress', legend=True, color='blue')
    ax.grid(True, which='major', axis='both')
    plt.axhline(0, color='r')
    plt.tight_layout()
    plt.savefig(os.path.join(common.basedir, 'DB Progress.pdf'))
    plt.close()


if __name__ == '__main__':
    run()