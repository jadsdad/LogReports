import pandas as pd
import logtools_common.logtools_common as common
import matplotlib.pylab as plt
import os

def run():
    fig, ax = plt.subplots(figsize=(15,7))
    sql = "select log.albumid as `Unqiue Albums Played`, min(log.logdate) as first_play from log inner join album on album.albumid = log.albumid where album.albumtypeid <> 16 group by log.albumid order by logdate asc;"
    total_sql = "select album.dateadded as `Date`, count(album.albumid) as `Total Albums in DB` from album where album.albumtypeid <> 16 group by dateadded;"
    alllogs_sql = "select log.logdate as logdate, count(log.logid) as `Total Plays` from log inner join album on album.albumid = log.albumid where album.albumtypeid <> 16 group by log.albumid order by logdate asc;"

    total_data = pd.read_sql(total_sql, common.conn)
    total_data['Date'] = pd.to_datetime(total_data['Date'])
    per = total_data['Date'].dt.to_period("D")
    totals = total_data.groupby([per]).sum().squeeze().cumsum()

    data = pd.read_sql(sql, common.conn)
    data['first_play'] = pd.to_datetime(data['first_play'])
    data = data.groupby(['first_play']).count()
    results = data.groupby(['first_play']).sum().squeeze().cumsum()

    all_logs_data = pd.read_sql(alllogs_sql, common.conn)
    all_logs_data['logdate'] = pd.to_datetime(all_logs_data['logdate'])
    all_logs_results = all_logs_data.groupby(['logdate']).sum().squeeze().cumsum()

    results.plot(ax=ax, legend=True, title = "Albums Played against Total")
    totals.plot(ax=ax, legend=True)
    all_logs_results.plot(ax=ax, legend=True)

    ax.grid(True, which='major', axis='both')
    plt.savefig(os.path.join(common.basedir, 'Albums Played against Total.pdf'))

if __name__ == '__main__':
    run()