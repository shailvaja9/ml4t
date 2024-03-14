from util import get_data, plot_data
import datetime as dt
import pandas as pd
from marketsimcode import compute_portvals, return_portvals
import matplotlib.pyplot as plt


class TheoreticallyOptimalStrategy:

	def author(self):
		return "svaja6"


	def testPolicy(self, symbol='AAPL', sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), sv=100000):
		data = get_data([symbol], pd.date_range(start=sd, end=ed))
		price_symbol = data[[symbol]]
		price_symbol= price_symbol.ffill().bfill()

		df_trades = pd.DataFrame( index= price_symbol.index.copy() , columns=[symbol])
		df_trades.fillna(0, inplace=True)
		df_trades.index.name = 'Date'
		current_position = 0
		for i in range(len(price_symbol) - 1):

			if price_symbol.iloc[i+1, 0] > price_symbol.iloc[i, 0]:
				action = 1000 - current_position
			else:
				action = -1000 - current_position
			df_trades.iloc[i,0] = action
			current_position += action

		portvals = compute_portvals(df_trades, sv, 0.0, 0.0)
		cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = return_portvals(portvals)
		print(cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio)
		return portvals

	def benchmark(self, symbol='AAPL', sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), sv=100000):
		data = get_data([symbol], pd.date_range(start=sd, end=ed))
		price_symbol = data[[symbol]]
		price_symbol = price_symbol.ffill().bfill()
		df_trades = pd.DataFrame(index=price_symbol.index.copy(), columns=[symbol])
		df_trades.fillna(0, inplace=True)
		df_trades.iloc[0,0] = 1000
		portvals = compute_portvals(df_trades, sv,0.0, 0.0)
		cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = return_portvals(portvals)
		print(cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio)
		return portvals

	def plot_graph(self, benchmark_portvals, tos_portvals):
		benchmark_portvals['value'] = benchmark_portvals['value'] / benchmark_portvals['value'][0]
		tos_portvals['value'] = tos_portvals['value'] / tos_portvals['value'][0]

		plt.figure(figsize=(14, 8))
		plt.title("TheoreticallyOptimalStrategy")


		#plt.xticks(rotation=30)
		#plt.grid()
		plt.plot(benchmark_portvals['value'], label="Benchmark", color="purple")
		plt.plot(tos_portvals['value'], label="TOS", color="red")
		plt.legend()
		plt.xlim(tos_portvals.index.min(), tos_portvals.index.max())

		plt.xlabel("Date")
		plt.ylabel("value")
		#plt.show()
		plt.savefig("images/theoretical.png", bbox_inches='tight')

		plt.clf()




