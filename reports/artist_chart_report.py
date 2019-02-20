import io
import os
from pathlib import Path
from datetime import date
import logtools_common.logtools_common as common

outdir = str(Path.home()) + "/Charts/Summaries"

def get_y_rank(artistid, yr):
    sql = "SELECT rank FROM chart_history WHERE artistid = {} AND y = {} AND Q = 0 AND albumid = 0;".format(artistid, yr)
    results = common.get_results(sql)
    if len(results) == 0:
        return None
    else:
        return results[0][0]

def get_q_rank(artistid, yr, qtr):
    sql = "SELECT rank FROM chart_history WHERE artistid = {} AND y = {} AND Q = {} AND albumid = 0;".format(artistid, yr, qtr)
    results = common.get_results(sql)
    if len(results) == 0:
        return None
    else:
        return results[0][0]

def annual(outfile):

    sql = "SELECT DISTINCT artist.artistid, artist.artistname, artist.sortname " \
          "FROM chart_history inner join artist on chart_history.artistid = artist.artistid " \
          "where Y <> 0 AND Q = 0 AND albumid = 0 " \
          "order by artist.sortname;"

    artist_list = common.get_results(sql)
    years = range(2018, date.today().year + 1)
    yrstring = "   ".join(str(y) for y in years)
    last_initial = ""
    outfile.write("{:<60}{}\n".format("",yrstring))
    for a in artist_list:
        artistid, artist, sortname = a
        initial = sortname[0].upper()
        yranks = []
        yrankstr = ""
        for y in years:
            yrank = get_y_rank(artistid, y)
            if yrank is None:
                yrankstr += "{:>7}".format("-")
            else:
                yrankstr += "{:>7}".format(yrank)

        linestr = "{:<63}{}".format(artist.upper(), yrankstr)
        if initial != last_initial:
            outfile.write("-" * len(linestr) + "\n")
        last_initial = initial
        outfile.write(linestr + "\n")


def seasonal(outfile):
    sql = "SELECT DISTINCT artist.artistid, artist.artistname, artist.sortname " \
          "FROM chart_history inner join artist on chart_history.artistid = artist.artistid " \
          "where Y <> 0 AND Q <> 0 AND albumid = 0 " \
          "order by artist.sortname;"

    artist_list = common.get_results(sql)
    years = range(2018, date.today().year + 1)
    quarters = range(1, 5)
    yrstring=""
    for y in years:
        for q in quarters:
            yrstring += "   " + "{}Q{}".format(y, q)
    last_initial = ""

    outfile.write("{:<60}{}\n".format("", yrstring))
    for a in artist_list:
        artistid, artist, sortname = a
        initial = sortname[0]
        yranks = []
        yrankstr = ""
        for y in years:
            for q in quarters:
                yrank = get_q_rank(artistid, y, q)
                if yrank is None:
                    yrankstr += "{:>9}".format("-")
                else:
                    yrankstr += "{:>9}".format(yrank)

        linestr = "{:<68}{}".format(artist.upper(), yrankstr)
        if initial != last_initial:
            outfile.write("-" * len(linestr) + "\n")
        last_initial = initial
        outfile.write(linestr + "\n")

def run():
    outfile = io.open(os.path.join(outdir, "Artist Chart Summary.txt"), "w", encoding='utf-8')
    outfile.write("ANNUAL")
    annual(outfile)
    outfile.write("\n\n\nSEASONAL")
    seasonal(outfile)

if __name__ == '__main__':
    run()
