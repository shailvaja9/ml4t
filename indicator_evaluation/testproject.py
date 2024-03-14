from util import get_data, plot_data
import datetime as dt
import pandas as pd
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt
from indicators import run
from TheoreticallyOptimalStrategy import TheoreticallyOptimalStrategy

def author():
    return "svaja6"

def report():
    sv = 100000
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    symbol = "JPM"
    tos = TheoreticallyOptimalStrategy()
    tos_data = tos.testPolicy(symbol, sd, ed, sv)
    benchmark_data = tos.benchmark(symbol, sd, ed, sv)
    tos.plot_graph(benchmark_data, tos_data)
    run()

if __name__ == "__main__":
    report()




