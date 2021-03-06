import matplotlib.pyplot as plt
from pathlib import Path
import logtools_common.logtools_common as common
from datetime import date

conn = common.conn

def query_db(sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def get_weekstats(y):
    sql = "SELECT * FROM listen_permonth where Y = {} order by m;".format(y)
    results = query_db(sql)
    return results

def run():
    outfile = str(Path.home()) + "/Charts/YOY Comparison.pdf"

    total = []

    plt.figure(figsize=(15, 7))

    for y in range(2018, date.today().year + 1):
        dataplot = []
        weekplot = []
        data = get_weekstats(y)
        for d in data:
            w = d[1]
            t = d[2]
            weekplot.append(w)
            dataplot.append(t)
            total.append(t)
        plt.plot(weekplot, dataplot, label=y)


    monthly_average = sum(total) / len(total)

    plt.title("Year-on-Year Comparison")
    plt.xlabel("Calendar Month")
    plt.ylabel("Time (hours)")
    plt.grid(axis='x', color='lightgrey', linestyle='--', markevery=3)
    plt.grid(axis='y', color='lightgrey', linestyle='--')
    plt.axis(xmin=1, xmax=12)
    plt.axhline(y=monthly_average, color='red', linestyle='--', lw=0.5)
    plt.legend(fontsize='x-small')
    plt.savefig(outfile, format="pdf")

if __name__ == '__main__':
    run()
