from reports import catalogue_report as catreport, stats_report as stats, TapeList as tape
from graphs import yoy_comparison_graph as yoy, monthly_media_graph as mmg

catreport.main()
mmg.run()
stats.main()
tape.generate_report(1.25)
yoy.run()
