import logtools_common.logtools_common as common
import io
from datetime import date, timedelta
from pathlib import Path

def get_plays_in_week(artistid, chart_date):

    startofweek = (chart_date - timedelta(weeks=13) + timedelta(days=1)).strftime("%Y-%m-%d")
    endofweek = chart_date.strftime("%Y-%m-%d")

    results = common.get_results("SELECT count(*) as logcount "
                                 "FROM log INNER JOIN albumartist ON albumartist.albumid = log.albumid "
                                 "INNER JOIN albumview ON albumartist.albumid = albumview.albumid "
                                 f"WHERE albumartist.artistid = {artistid} and log.logdate between '{startofweek}' and '{endofweek}';")

    return results[0][0]

def run():
    conn = common.conn
    seperator = "\n\n" + ("-" * 120) + "\n"

    results = common.get_results("SELECT artist.artistid, artist.artistname, chr.chartdate, chr.rank, chr.chartrun "
                                    "FROM artist INNER JOIN chart_history_rolling chr "
                                    "ON artist.artistid = chr.artistid "
                                    "ORDER BY artist.sortname, chr.chartdate;")

    out = io.open(str(Path.home()) + "\Charts\Rolling Artist Stats.txt","w", encoding='utf-8')

    last_artist = ""
    last_run = 0
    last_rank = 99

    for r in results:
        artistid, artist, chartdate, rank, run = r
        indicator = ""

        if artist != last_artist:
            out.write(seperator)
            out.write(artist.upper() + "\n")
            last_artist = artist
            last_run = 0
            last_rank = 99

        if run > last_run:
            out.write("\n")
            indicator = "N" if last_run == 0 else "R"
            last_run = run
            last_rank = 99

        if rank == 1:
            indicator += "*"
        elif rank < last_rank and indicator == "":
            indicator = "+"

        plays = get_plays_in_week(artistid, chartdate)

        linestr = "\t\t{:<25}{:>5}{:>5}{:>10}{}\n".format(chartdate.strftime("%Y-%b-%d"), rank, indicator,
                                                        "", "*" * plays if plays > 0 else "")
        out.write(linestr)
        last_rank = rank

    out.flush()
    out.close()

if __name__ == '__main__':
    run()