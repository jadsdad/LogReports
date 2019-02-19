from reports import catalogue_report as catreport, stats_report as stats, TapeList as tape
from graphs import yoy_comparison_graph as yoy, \
    monthly_media_graph as mmg, \
    Art_Freq_Graphs as afg, \
    catalogue_size as catsize, \
    year_of_release as yor, \
    media_by_year as mby, \
    albums_played_against_total as apat, \
    db_growth as growth, albums_by_length as abl, \
    albums_by_timesplayed as abtp

from datetime import date


from multiprocessing import Pool

def execute(routine):
    routine()

def run():
    report_routines = [catreport.main(),
                       mmg.run(),
                       stats.main(),
                       tape.generate_report(1.25),
                       yoy.run(),
                       catsize.run(),
                       yor.run(),
                       mby.run(),
                       apat.run(),
                       growth.run(),
                       abl.run(),
                       abtp.run()]

    p = Pool(4)
    p.map_async(execute, report_routines)

    if date.today().weekday() == 6:
        afg.run()

if __name__ == '__main__':
    run()
