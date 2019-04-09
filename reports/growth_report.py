import logtools_common.logtools_common as common
import os
import io
from datetime import date, timedelta

conn = common.conn
thresh_date = (date.today() - timedelta(weeks=13)).strftime("%Y-%m-%d")

def run():

    sql = "Select * from (select 'Added' as Status, cast(album.dateadded as date) as `Date`, album.artistcredit as Artist, " \
          "album.album as Title from albumview as album " \
          "UNION " \
          "select 'Played' as status, min(log.logdate) as `Date`, album.artistcredit as Artist, album.album as title " \
          "from log inner join albumview as album on album.albumid = log.albumid " \
          "group by log.albumid) x " \
          f"where `Date` >= '{thresh_date}' " \
          "order by `Date`, Status, Artist, Title;"

    results = common.get_results(sql)
    outfile = os.path.join(common.basedir, "Growth Report.txt")
    out = io.open(outfile,"w", encoding='utf-8')

    last_date = date(1990,1,1)
    progress = 0
    positive = 0
    neutral = 0
    negative = 0
    overall = 0

    for r in results:
        status, dt, artist, album = r
        if dt > last_date:
            dts = dt.strftime("%Y-%b-%d")
            if last_date != date(1990,1,1):
                out.write(f"\n\tProgress: {progress}\n")
            out.write(f"\n{dts}\n\n")
            last_date = dt
            positive += 1 if progress > 0 else 0
            neutral += 1 if progress == 0 else 0
            negative += 1 if progress < 0 else 0
            overall += progress

            progress = 0

        out.write(f"\t{status.upper()}\t{artist}: {album}\n")
        progress += 1 if status == 'Played' else -1

    out.write(f"\nPositive Progress:\t{positive}\n")
    out.write(f"Neutral Progress:\t{neutral}\n")
    out.write(f"Negative Progress:\t{negative}\n")

    out.write(f"\n13 Week Progress:\t{overall}\n")

    out.flush()
    out.close()


if __name__ == '__main__':
    run()



