import io
import os
from pathlib import Path
from datetime import date
import logtools_common.logtools_common as common

outdir = str(Path.home()) + "/Charts/Summaries"

def get_y_rank(albumid, yr):
    sql = "SELECT rank FROM chart_history WHERE albumid = {} AND y = {} AND Q = 0 and tyr=0;".format(albumid, yr)
    results = common.get_results(sql)
    if len(results) == 0:
        return None
    else:
        return results[0][0]

def get_q_rank(albumid, yr, qtr):
    sql = "SELECT rank FROM chart_history WHERE albumid = {} AND y = {} AND Q = {};".format(albumid, yr, qtr)
    results = common.get_results(sql)
    if len(results) == 0:
        return None
    else:
        return results[0][0]

def annual(outfile):

    sql = "SELECT DISTINCT artist.artistid, artist.artistname, artist.sortname, album.albumid, album.album " \
          "FROM chart_history inner join albumartist on chart_history.albumid = albumartist.albumid " \
          "INNER JOIN album on albumartist.albumid = album.albumid " \
          "INNER JOIN artist on albumartist.artistid = artist.artistid " \
          "where Y <> 0 AND Q = 0 and tyr = 0 " \
          "order by artist.sortname, album.album;"

    artist_list = common.get_results(sql)
    years = range(2018, date.today().year + 1)
    yrstring = "   ".join(str(y) for y in years)
    last_initial = ""
    outfile.write("{:<60}{}\n".format("",yrstring))
    for a in artist_list:
        artistid, artist, sortname, albumid, album = a
        initial = sortname[0].upper()
        yranks = []
        yrankstr = ""
        for y in years:
            yrank = get_y_rank(albumid, y)
            if yrank is None:
                yrankstr += "{:>7}".format("-")
            else:
                yrankstr += "{:>7}".format(yrank)

        linestr = "{:<63}{}".format((artist.upper() + ": " + album)[:60], yrankstr)
        if initial != last_initial:
            outfile.write("-" * len(linestr) + "\n")
        last_initial = initial
        outfile.write(linestr + "\n")


def seasonal(outfile):
    sql = "SELECT DISTINCT artist.artistid, artist.artistname, artist.sortname, album.albumid, album.album " \
          "FROM chart_history inner join albumartist on chart_history.albumid = albumartist.albumid " \
          "INNER JOIN album on albumartist.albumid = album.albumid " \
          "INNER JOIN artist on albumartist.artistid = artist.artistid " \
          "where Y <> 0 AND Q <> 0 " \
          "order by artist.sortname, album.album;"

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
        artistid, artist, sortname, albumid, album = a
        initial = sortname[0]
        yranks = []
        yrankstr = ""
        for y in years:
            for q in quarters:
                yrank = get_q_rank(albumid, y, q)
                if yrank is None:
                    yrankstr += "{:>9}".format("-")
                else:
                    yrankstr += "{:>9}".format(yrank)

        linestr = "{:<68}{}".format((artist.upper() + ": " + album)[:60], yrankstr)
        if initial != last_initial:
            outfile.write("-" * len(linestr) + "\n")
        last_initial = initial
        outfile.write(linestr + "\n")

def run():
    if not os.path.exists(outdir):
        os.mkdir(outdir)
        
    outfile = io.open(os.path.join(outdir, "Album Chart Summary.txt"), "w", encoding='utf-8')
    outfile.write("ANNUAL")
    annual(outfile)
    outfile.write("\n\n\nSEASONAL")
    seasonal(outfile)

if __name__ == '__main__':
    run()
