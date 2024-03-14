""""""  		  	   		  		 		  		  		    	 		 		   		 		  
"""MC1-P2: Optimize a portfolio.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
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
  		  	   		  		 		  		  		    	 		 		   		 		  
import numpy as np

import pandas as pd
from assess_learners.util import get_data
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import os

# This is the function that will be tested by the autograder  		  	   		  		 		  		  		    	 		 		   		 		  
# The student must update this code to properly implement the functionality  		  	   		  		 		  		  		    	 		 		   		 		  
def optimize_portfolio(  		  	   		  		 		  		  		    	 		 		   		 		  
    sd=dt.datetime(2010, 1, 1),
    ed=dt.datetime(2010, 12, 31),
    syms=["GOOG", "AAPL", "GLD", "XOM"],
    gen_plot=False,  		  	   		  		 		  		  		    	 		 		   		 		  
):  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    This function should find the optimal allocations for a given set of stocks. You should optimize for maximum Sharpe  		  	   		  		 		  		  		    	 		 		   		 		  
    Ratio. The function should accept as input a list of symbols as well as start and end dates and return a list of  		  	   		  		 		  		  		    	 		 		   		 		  
    floats (as a one-dimensional numpy array) that represents the allocations to each of the equities. You can take  		  	   		  		 		  		  		    	 		 		   		 		  
    advantage of routines developed in the optional assess portfolio project to compute daily portfolio value and  		  	   		  		 		  		  		    	 		 		   		 		  
    statistics.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
    :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		  		 		  		  		    	 		 		   		 		  
    :type sd: datetime  		  	   		  		 		  		  		    	 		 		   		 		  
    :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		  		 		  		  		    	 		 		   		 		  
    :type ed: datetime  		  	   		  		 		  		  		    	 		 		   		 		  
    :param syms: A list of symbols that make up the portfolio (note that your code should support any  		  	   		  		 		  		  		    	 		 		   		 		  
        symbol in the data directory)  		  	   		  		 		  		  		    	 		 		   		 		  
    :type syms: list  		  	   		  		 		  		  		    	 		 		   		 		  
    :param gen_plot: If True, optionally create a plot named plot.png. The autograder will always call your  		  	   		  		 		  		  		    	 		 		   		 		  
        code with gen_plot = False.  		  	   		  		 		  		  		    	 		 		   		 		  
    :type gen_plot: bool  		  	   		  		 		  		  		    	 		 		   		 		  
    :return: A tuple containing the portfolio allocations, cumulative return, average daily returns,  		  	   		  		 		  		  		    	 		 		   		 		  
        standard deviation of daily returns, and Sharpe ratio  		  	   		  		 		  		  		    	 		 		   		 		  
    :rtype: tuple  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
    # Read in adjusted closing prices for given symbols, date range  		  	   		  		 		  		  		    	 		 		   		 		  
    dates = pd.date_range(sd, ed)  		  	   		  		 		  		  		    	 		 		   		 		  
    prices_all = get_data(syms, dates)  # automatically adds SPY  		  	   		  		 		  		  		    	 		 		   		 		  
    prices = prices_all[syms]  # only portfolio symbols  		  	   		  		 		  		  		    	 		 		   		 		  
    prices_SPY = prices_all["SPY"]  # only SPY, for comparison later  		  	   		  		 		  		  		    	 		 		   		 		  
    prices_SPY = prices_SPY/prices_SPY.iloc[0]
    # find the allocations for the optimal portfolio  		  	   		  		 		  		  		    	 		 		   		 		  
    # note that the values here ARE NOT meant to be correct for a test case  		  	   		  		 		  		  		    	 		 		   		 		  
    allocs = np.asarray(  		  	   		  		 		  		  		    	 		 		   		 		  
        [0.2, 0.2, 0.3, 0.3]  		  	   		  		 		  		  		    	 		 		   		 		  
    )  # add code here to find the allocations  		  	   		  		 		  		  		    	 		 		   		 		  
    cr, adr, sddr, sr = [  		  	   		  		 		  		  		    	 		 		   		 		  
        0.25,  		  	   		  		 		  		  		    	 		 		   		 		  
        0.001,  		  	   		  		 		  		  		    	 		 		   		 		  
        0.0005,  		  	   		  		 		  		  		    	 		 		   		 		  
        2.1,  		  	   		  		 		  		  		    	 		 		   		 		  
    ]  # add code here to compute stats
    sv = 1
    normalized_prices = prices/prices.iloc[0,:]

    def optimzation_func(allocs, normalized_return):
        allocated = normalized_return*allocs
        position_values = allocated*sv
        position_values['Total'] = position_values.sum(axis=1)




    # Get daily portfolio value
        position_values['Daily Returns'] = position_values['Total'].pct_change(1)
        portfolio_daily_return_mean = position_values['Daily Returns'].mean()
        sddr = position_values['Daily Returns'].std()
        cr = 100*(position_values['Total'][-1]/position_values['Total'][0] -1)
        sr = portfolio_daily_return_mean / sddr
        annualized_sharpe_ratio = sr * (252**0.5)
        return annualized_sharpe_ratio*-1


    cons = ({'type':'eq', 'fun': lambda x: np.sum(x) -1})
    bounds= tuple((0,1) for x in range(len(syms)))
    #nsr = annualized_sharpe_ratio *-1
    allocs_i = [1./len(syms)]*len(syms)


    result = minimize(optimzation_func, allocs_i, args=(normalized_prices), method = 'SLSQP', bounds = bounds, constraints=cons)
    new_alloc = result.x




    allocated = normalized_prices*new_alloc
    position_values = allocated*sv
    position_values['Total'] = position_values.sum(axis=1)



  		  	   		  		 		  		  		    	 		 		   		 		  
    # Get daily portfolio value
    position_values['Daily Returns'] = position_values['Total'].pct_change(1)
    portfolio_daily_return_mean = position_values['Daily Returns'].mean()
    sddr = position_values['Daily Returns'].std()
    cr = 100*(position_values['Total'][-1]/position_values['Total'][0] -1)
    sr = portfolio_daily_return_mean / sddr
    sr = sr * (252**0.5)

    def plot(title, xlabel, ylabel, list_of_ndarray, list_of_label, filename):

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        my_path = os.path.dirname(__file__)

        for i in range(len(list_of_ndarray)):
            if len(list_of_label) == len(list_of_ndarray):
                plt.plot(list_of_ndarray[i],label = str(list_of_label[i]))
            else:
                plt.plot(list_of_ndarray[i])
            plt.legend()

        filename = os.path.join(my_path, "images",filename)
        plt.savefig(filename)
        plt.clf()



    #port_val = prices_SPY  # add code here to compute daily portfolio values
  		  	   		  		 		  		  		    	 		 		   		 		  
    # Compare daily portfolio value with SPY using a normalized plot  		  	   		  		 		  		  		    	 		 		   		 		  
    if gen_plot:  		  	   		  		 		  		  		    	 		 		   		 		  
        # add code to plot here
        plot('Portfolio_vs_SPY','Date', 'Price', [position_values['Total'] , prices_SPY], ['Portfolio', 'SPY'], 'portfolio_vs_spy')
  		  	   		  		 		  		  		    	 		 		   		 		  
    return new_alloc, cr, adr, sddr, sr
  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
def test_code():  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    This function WILL NOT be called by the auto grader.  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
    start_date = dt.datetime(2008, 6, 1)
    end_date = dt.datetime(2009, 6, 1)
    symbols = ["IBM", "X", "GLD", "JPM"]
  		  	   		  		 		  		  		    	 		 		   		 		  
    # Assess the portfolio  		  	   		  		 		  		  		    	 		 		   		 		  
    allocations, cr, adr, sddr, sr = optimize_portfolio(  		  	   		  		 		  		  		    	 		 		   		 		  
        sd=start_date, ed=end_date, syms=symbols, gen_plot=True
    )  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
    # Print statistics  		  	   		  		 		  		  		    	 		 		   		 		  
    print(f"Start Date: {start_date}")  		  	   		  		 		  		  		    	 		 		   		 		  
    print(f"End Date: {end_date}")  		  	   		  		 		  		  		    	 		 		   		 		  
    print(f"Symbols: {symbols}")  		  	   		  		 		  		  		    	 		 		   		 		  
    print(f"Allocations:{allocations}")  		  	   		  		 		  		  		    	 		 		   		 		  
    print(f"Sharpe Ratio: {sr}")  		  	   		  		 		  		  		    	 		 		   		 		  
    print(f"Volatility (stdev of daily returns): {sddr}")  		  	   		  		 		  		  		    	 		 		   		 		  
    print(f"Average Daily Return: {adr}")  		  	   		  		 		  		  		    	 		 		   		 		  
    print(f"Cumulative Return: {cr}")  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		  		 		  		  		    	 		 		   		 		  
    # This code WILL NOT be called by the auto grader  		  	   		  		 		  		  		    	 		 		   		 		  
    # Do not assume that it will be called  		  	   		  		 		  		  		    	 		 		   		 		  
    test_code()  		  	   		  		 		  		  		    	 		 		   		 		  
