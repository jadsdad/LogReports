import logtools_common.logtools_common as common
import pandas as pd
import matplotlib.pylab as plt
import matplotlib.dates as mdates
import os
from matplotlib.backends.backend_pdf import PdfPages
from datetime import date


def run():
    conn = common.conn
    date_range = pd.date_range('2018-01-01', date.today())
    artistcount = int(common.total_artists() * 0.05)

    logcount_sql = "SELECT artist.artistname, count(logid) as logcount " \
                   "FROM artist " \
                   "INNER JOIN albumartist ON artist.artistid = albumartist.artistid " \
                   "INNER JOIN log ON log.albumid = albumartist.albumid " \
                   "GROUP BY artistname " \
                   "ORDER BY logcount desc;"

    logdate_sql = "SELECT DISTINCT log.logdate, artist.artistname " \
                  "FROM artist " \
                  "INNER JOIN albumartist ON artist.artistid = albumartist.artistid " \
                  "INNER JOIN log on log.albumid = albumartist.albumid;"

    logcount_data = pd.read_sql(logcount_sql, conn)
    logdate_data = pd.read_sql(logdate_sql, conn, index_col='logdate')
    logcount_data = logcount_data[:artistcount].sort_values(by='artistname', ascending=True)
    artist_list = logcount_data['artistname'].tolist()
    logdate_data = logdate_data[logdate_data['artistname'].isin(logcount_data['artistname'])].sort_index()

    with PdfPages(os.path.join(common.basedir, 'Frequency Graphs.pdf')) as pp:
        for a in artist_list:
            print(a)
            this_artist = logdate_data[logdate_data['artistname'] == a]
            this_artist['played'] = 1
            this_artist = this_artist.reindex(date_range, fill_value=0)

            plt.rcParams.update({'font.size': 20})
            plt.rcParams.update({'font.family': 'monospace'})

            fig, ax = plt.subplots(figsize=(30, 15))

            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%y'))
            ax.yaxis.label.set_visible(False)
            ax.grid('on', which='major', axis='x')

            plt.title(a.upper())

            ax.bar(this_artist.index, this_artist['played'])

            pp.savefig(fig)
            plt.close()

if __name__ == '__main__':
    run()