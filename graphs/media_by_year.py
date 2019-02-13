import pandas as pd
import logtools_common.logtools_common as common
import matplotlib.pylab as plt
import os

def run():
    sql = "SELECT album.yearreleased as `Year of Release`, source.Source, count(albumid) as Albums " \
          "FROM album inner join source on album.SourceID = source.SourceID " \
          "where album.albumtypeid<>16 group by album.yearreleased, source.Source " \
          "order by album.yearreleased, source.Source;"
    
    data = pd.read_sql(sql, common.conn)
    results = data.groupby(['Year of Release','Source']).sum()
    graph_results = results['Albums'].unstack().fillna(0)
    graph_results.plot(kind='bar', title="Albums by Year & Media", figsize=(20,25), subplots=True, sharex=True, sharey=True)
    plt.tight_layout()
    plt.savefig(os.path.join(common.basedir, 'Media by Year Graphs.pdf'))
    plt.close()

if __name__ == '__main__':
    run()