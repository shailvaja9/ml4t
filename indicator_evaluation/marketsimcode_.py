""""""  		  	   		 	   			  		 			     			  	 
"""MC2-P1: Market simulator.  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		 	   			  		 			     			  	 
Atlanta, Georgia 30332  		  	   		 	   			  		 			     			  	 
All Rights Reserved  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
Template code for CS 4646/7646  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		 	   			  		 			     			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		 	   			  		 			     			  	 
and other users of this template code are advised not to share it with others  		  	   		 	   			  		 			     			  	 
or to make it available on publicly viewable websites including repositories  		  	   		 	   			  		 			     			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		 	   			  		 			     			  	 
or edited.  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
We do grant permission to share solutions privately with non-students such  		  	   		 	   			  		 			     			  	 
as potential employers. However, sharing with other current or future  		  	   		 	   			  		 			     			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		 	   			  		 			     			  	 
GT honor code violation.  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
-----do not edit anything above this line---  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
Student Name: Tucker Balch (replace with your name)  		  	   		 	   			  		 			     			  	 
GT User ID: tb34 (replace with your User ID)  		  	   		 	   			  		 			     			  	 
GT ID: 900897987 (replace with your GT ID)  		  	   		 	   			  		 			     			  	 
"""  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
import datetime as dt  		  	   		 	   			  		 			     			  	 
import os  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
import numpy as np  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
import pandas as pd  		  	   		 	   			  		 			     			  	 
from util import get_data, plot_data
import datetime
  		  	   		 	   			  		 			     			  	 

def author():
    return 'svaja6'

def closing_prices(orders):
    start_date = orders.index.min()
    end_date = orders.index.max()
    #symbols = orders['Symbol']
    #symbols = list(set(symbols))
    return start_date, end_date

def get_closing_price(symbol, date, prices):
    date = datetime.datetime.strptime(date, r'%Y-%m-%d')
    return prices.at[date,symbol]

def get_orders_for_date(date, orders):
    return  [row.tolist() for _, row in orders.loc[orders.index == str(date)].iterrows()]


def get_value(commission, impact, price, quantity, order_type):
    if order_type == 'BUY':
        order_value = ((price*(1.00+impact)) * quantity) + commission
        return (order_value * -1.00)
    if order_type == 'SELL':
        order_value = ((price*(1.00-impact)) * quantity) - commission
        return (order_value * 1.00)

def check_port_value(current_portfolio, prices, date):
    date = datetime.datetime.strptime(date, r'%Y-%m-%d')

    for key, value in current_portfolio.items():
        if key != 'cash':
            price = prices.at[date, key]
            value['value'] = price * abs(value['quantity'])

    portfolio_value = 0.0
    for val in current_portfolio.values():
        portfolio_value += val['value']

    return portfolio_value





def return_portvals(portvals):
    #print(portvals)
    portvals['Daily Returns'] = portvals['Value'].pct_change(1)
    portfolio_daily_return_mean = portvals['Daily Returns'].mean()
    sddr = portvals['Daily Returns'].std()
    cr = 100 * (portvals['Value'][-1] / portvals['Value'][0] - 1)
    sr = portfolio_daily_return_mean / sddr
    sr = sr * (252 ** 0.5)
    return cr, portfolio_daily_return_mean,sddr, sr



def compute_portvals(
    orders ,
    start_val=1000000.00,
    commission=9.95,
    impact=0.005,
):  		  	   		 	   			  		 			     			  	 
    """  		  	   		 	   			  		 			     			  	 
    Computes the portfolio values.  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
    :param orders_file: Path of the order file or the file object  		  	   		 	   			  		 			     			  	 
    :type orders_file: str or file object  		  	   		 	   			  		 			     			  	 
    :param start_val: The starting value of the portfolio  		  	   		 	   			  		 			     			  	 
    :type start_val: int  		  	   		 	   			  		 			     			  	 
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		 	   			  		 			     			  	 
    :type commission: float  		  	   		 	   			  		 			     			  	 
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		 	   			  		 			     			  	 
    :type impact: float  		  	   		 	   			  		 			     			  	 
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		 	   			  		 			     			  	 
    :rtype: pandas.DataFrame  		  	   		 	   			  		 			     			  	 
    """  		  	   		 	   			  		 			     			  	 
    # this is the function the autograder will call to test your code  		  	   		 	   			  		 			     			  	 
    # NOTE: orders_file may be a string, or it may be a file object. Your  		  	   		 	   			  		 			     			  	 
    # code should work correctly with either input  		  	   		 	   			  		 			     			  	 
    # TODO: Your code here




    #orders = orders.set_index('Date', inplace=True)
    symbol = "JPM"
    start_date, end_date = closing_prices(orders)
    #orders.set_index('Date', inplace=True)

    prices = get_data([symbol], pd.date_range(start_date, end_date))
    prices.index.name = 'Date'
    prices.drop('SPY', axis=1, inplace=True)
    #print(prices.describe())
    #prices.set_index('Date', inplace=True)
    portvals = pd.DataFrame( index= prices.index.copy() , columns=['value'])
    portvals['value'] = portvals['value'].astype(float)
    #portvals.index = prices.index.copy()
   # portvals = portvals["Date"].reset_index(drop=True)
    current_portfolio = {'cash':{'quantity':0, 'value': start_val}, symbol: {'quantity':0, 'value':0}}
    #portvals.set_index('Date', inplace=True)
    portvals["value"].fillna(0, inplace=True)
    portvals["value"].iloc[0] = start_val
    updated_value = start_val
    portvals.index = portvals.index.strftime('%Y-%m-%d')
    cost_of_trade = 0
    for index, row in portvals.iterrows():
        trade = orders.loc[index][symbol]

        #check if date exists in order
        #index = datetime.datetime.fromtimestamp(index)
        #index = datetime.datetime.strptime(index, '%Y-%m-%d')
        #if str(index) in orders.index:

            #order_num = get_orders_for_date(index, orders)
            #for order in order_num:
                #if symbol in current_portfolio:
        if trade > 0:
            #cost_of_trade -=get_value(commission, impact, prices.loc[index][symbol], current_portfolio[symbol]['quantity'], "SELL")
            cost_of_trade = get_value(commission, impact, prices.loc[index][symbol], current_portfolio[symbol]['quantity'], "SELL") -  get_value(commission, impact, prices.loc[index][symbol],  current_portfolio[symbol]['quantity']+trade, "BUY")
            current_portfolio[symbol]['quantity'] += trade
            current_portfolio['cash']['value']+=cost_of_trade
            cost_of_trade = 0
        if trade < 0:
            cost_of_trade =  get_value(commission, impact, prices.loc[index][symbol], abs(current_portfolio[symbol]['quantity']+trade), "SELL") - get_value(commission, impact, prices.loc[index][symbol], current_portfolio[symbol]['quantity'], "BUY")

            current_portfolio[symbol]['quantity'] += trade
            current_portfolio['cash']['value'] += cost_of_trade
            cost_of_trade = 0
        portvals.at[index, "value"] = check_port_value(current_portfolio, prices, index)

    #portvals.index.name = 'Date'

    return portvals
  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
def test_code():  		  	   		 	   			  		 			     			  	 
    """  		  	   		 	   			  		 			     			  	 
    Helper function to test code  		  	   		 	   			  		 			     			  	 
    """  		  	   		 	   			  		 			     			  	 
    # this is a helper function you can use to test your code  		  	   		 	   			  		 			     			  	 
    # note that during autograding his function will not be called.  		  	   		 	   			  		 			     			  	 
    # Define input parameters  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
    of = "./orders/orders-10.csv"
    sv = 1000000.00
  		  	   		 	   			  		 			     			  	 
    # Process orders  		  	   		 	   			  		 			     			  	 
    portvals = compute_portvals(orders_file=of, start_val=sv)
    start_date = portvals.iloc[0]
    end_date = portvals.iloc[-1]
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = return_portvals(portvals)

    if isinstance(portvals, pd.DataFrame):  		  	   		 	   			  		 			     			  	 
        portvals = portvals[portvals.columns[0]]  # just get the first column  		  	   		 	   			  		 			     			  	 
    else:  		  	   		 	   			  		 			     			  	 
        "warning, code did not return a DataFrame"  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
    # Get portfolio stats  		  	   		 	   			  		 			     			  	 
    # Here we just fake the data. you should use your code from previous assignments.  		  	   		 	   			  		 			     			  	 
    #start_date = dt.datetime(2008, 1, 1)
    #end_date = dt.datetime(2008, 6, 1)
    #cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [
    #    0.2,
    #    0.01,
    #    0.02,
    #    1.5,
    #]



    # Compare portfolio against $SPX  		  	   		 	   			  		 			     			  	 
    print(f"Date Range: {start_date} to {end_date}")  		  	   		 	   			  		 			     			  	 
    print()  		  	   		 	   			  		 			     			  	 
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")  		  	   		 	   			  		 			     			  	 
    #print(f"Sharpe Ratio of SPY : {sharpe_ratio_SPY}")
    print()  		  	   		 	   			  		 			     			  	 
    print(f"Cumulative Return of Fund: {cum_ret}")  		  	   		 	   			  		 			     			  	 
    #print(f"Cumulative Return of SPY : {cum_ret_SPY}")
    print()  		  	   		 	   			  		 			     			  	 
    print(f"Standard Deviation of Fund: {std_daily_ret}")  		  	   		 	   			  		 			     			  	 
    #print(f"Standard Deviation of SPY : {std_daily_ret_SPY}")
    print()  		  	   		 	   			  		 			     			  	 
    print(f"Average Daily Return of Fund: {avg_daily_ret}")  		  	   		 	   			  		 			     			  	 
    #print(f"Average Daily Return of SPY : {avg_daily_ret_SPY}")
    print()  		  	   		 	   			  		 			     			  	 
    print(f"Final Portfolio value: {portvals[-1]}")
  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
if __name__ == "__main__":  		  	   		 	   			  		 			     			  	 
    test_code()  		  	   		 	   			  		 			     			  	 
