import pandas as pd
import logtools_common.logtools_common as common
import matplotlib.pylab as plt
import os

from matplotlib.backends.backend_pdf import PdfPages
from datetime import date

def run():
    lengths = pd.Series(range(1, 121))
    fig, ax = plt.subplots(figsize=(15,7))

    sql = "select cast(round(albumlength / 60) as int) as RT, count(albumid) as `Albums`, " \
          "sum(if(playcount=0, 0, 1)) as Played from albumlengths where cast(round(albumlength / 60) as int) <= 120 " \
          "group by RT;"

    data = pd.read_sql(sql, common.conn, index_col='RT')
    data = data.reindex(lengths)
    data.fillna(0).plot(ax=ax, title='Albums by Length')
    ax.grid(True, which='major', axis='both')
    plt.savefig(os.path.join(common.basedir, 'Albums by Length.pdf'))

if __name__ == '__main__':
    run()
