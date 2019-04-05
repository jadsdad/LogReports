import logtools_common.logtools_common as common
import io
from pathlib import Path

conn = common.conn
seperator = "\n\n" + ("-" * 120) + "\n"

results = common.get_results("SELECT artist.artistname, chr.chartdate, chr.rank, chr.chartrun "
                                "FROM artist INNER JOIN chart_history_rolling chr "
                                "ON artist.artistid = chr.artistid "
                                "ORDER BY artist.sortname, chr.chartdate;")

out = io.open(str(Path.home()) + "\Test.txt","w", encoding='utf-8')

last_artist = ""
last_run = 0
last_rank = 99

for r in results:
    artist, chartdate, rank, run = r
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

    linestr = "\t\t{:<25}{:>5}{:>5}\n".format(chartdate.strftime("%Y-%b-%d"), rank, indicator)
    out.write(linestr)
    last_rank = rank

out.flush()
out.close()

