import pandas as pd
import logtools_common.logtools_common as common
import matplotlib.pylab as plt
import os

def run():
    sql = "select album.PlayCount as Played, count(album.AlbumID) as Albums " \
          "from album group by album.PlayCount order by album.PlayCount"

    pcdata = pd.read_sql(sql, common.conn, index_col='Played')

    fig, ax = plt.subplots(figsize=(15,10))
    pcdata.plot(ax=ax, title='Albums by # Times Played')
    ax.grid(True, which='major', axis='both')
    plt.savefig(os.path.join(common.basedir, 'Albums by Times Played.pdf'))

if __name__ == '__main__':
    run()
