""""""  		  	   		  		 		  		  		    	 		 		   		 		  
"""Assess a betting strategy.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
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

  		  	   		  		 		  		  		    	 		 		   		 		  
import numpy as np
import matplotlib.pyplot as plt
import os
  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
def author():  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    :return: The GT username of the student  		  	   		  		 		  		  		    	 		 		   		 		  
    :rtype: str  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    return "svaja6"  # replace tb34 with your Georgia Tech username.
  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
def gtid():  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    :return: The GT ID of the student  		  	   		  		 		  		  		    	 		 		   		 		  
    :rtype: int  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    return 903953102  # replace with your GT ID number
  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
def get_spin_result(win_prob):  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    Given a win probability between 0 and 1, the function returns whether the probability will result in a win.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
    :param win_prob: The probability of winning  		  	   		  		 		  		  		    	 		 		   		 		  
    :type win_prob: float  		  	   		  		 		  		  		    	 		 		   		 		  
    :return: The result of the spin.  		  	   		  		 		  		  		    	 		 		   		 		  
    :rtype: bool  		  	   		  		 		  		  		    	 		 		   		 		  
    """
    result = False  		  	   		  		 		  		  		    	 		 		   		 		  
    if np.random.random() <= win_prob:  		  	   		  		 		  		  		    	 		 		   		 		  
        result = True  		  	   		  		 		  		  		    	 		 		   		 		  
    return result  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
def test_code():  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    Method to test your code  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    win_prob = 9/19  # set appropriately to the probability of a win
    np.random.seed(gtid())  # do this only once
    fig1(win_prob)
    fig2(win_prob)
    fig3(win_prob)
    bankroll = 256
    fig4(win_prob, bankroll)
    fig5(win_prob, bankroll)
    #print(get_spin_result(win_prob))  # test the roulette spin
    # add your code here to implement the experiments  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  

def simulator(win_prob, has_bank_roll = False, bankroll = 0 ):
    #setting initial value to 80 so when the winning cap is reached we dont need to populate the rest
    res = np.full((1001), 80)
    episode_winnings = 0
    count = 0
    while episode_winnings < 80:
        won = False
        bet_amount = 1
        while not won:
            if count >=1001:
                return res
            res[count] = episode_winnings
            count+=1
            won = get_spin_result(win_prob)
            if won == True:
                episode_winnings = episode_winnings + bet_amount
            else:
                episode_winnings = episode_winnings - bet_amount
                bet_amount = bet_amount * 2
                if has_bank_roll:
                    if episode_winnings == -bankroll:
                        res[count:] = episode_winnings
                        return res

                    if episode_winnings - bet_amount < -bankroll:
                        bet_amount = bankroll + episode_winnings

    return res

def plot(title, xlabel, ylabel, list_of_ndarray, list_of_label, filename):
    plt.axis([0, 300, -256, 100])
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



def fig1(win_prob):


    list_array = []

    for index in range(10): #10 episodes
        curr_episode = simulator(win_prob)
        list_array.append(curr_episode)

    plot("Fig1 - 10 Episodes Without Bankroll", "Trials", "Winnings", list_array, [], "Fig-1")






def fig2(win_prob):
    list_array = []
    result = np.zeros((1000,1001))

    for index in range(1000): #1000 episodes

        curr_episode = simulator(win_prob)
        result[index] = curr_episode

    mean = np.mean(result, axis=0)
    std = np.std(result, axis=0)
    list_array.append(mean+std)
    list_array.append(mean)
    list_array.append(mean-std)

    plot("Fig2-1000 Episodes Without Bankroll with Mean", "Episodes", "Winnings", list_array, ["Mean-Std","Mean","Mean+Std"], "Fig-2")


def fig3(win_prob):
    list_array = []
    result = np.zeros((1000,1001))

    for index in range(1000):

        curr_episode = simulator(win_prob)
        result[index] = curr_episode

    median = np.median(result, axis=0)
    std = np.std(result, axis=0)
    list_array.append(median+std)
    list_array.append(median)
    list_array.append(median-std)


    plot("Fig3-1000 Episodes Without Bankroll with Median", "Episodes", "Winnings", list_array, ["Median-Std","Median","Median+Std"], "Fig-3")


def fig4(win_prob, bankroll):
    list_array = []
    result = np.zeros((1000,1001))

    for index in range(1000):

        curr_episode = simulator(win_prob, True, bankroll)
        result[index] = curr_episode

    mean = np.mean(result, axis=0)
    std = np.std(result, axis=0)
    list_array.append(mean+std)
    list_array.append(mean)
    list_array.append(mean-std)
    #count_of_busts = np.min(result, axis=0)
    #count_of_busts = np.count_nonzero(count_of_busts < -256)
    #count_of_winning_cap = np.max(result, axis=0)

    plot("Fig4-1000 Episodes With Bankroll with Mean", "Episodes", "Winnings", list_array, ["Mean-Std","Mean","Mean+Std"],"Fig-4")



def fig5(win_prob, bankroll):
    list_array = []
    result = np.zeros((1000,1001))

    for index in range(1000):

        curr_episode = simulator(win_prob, True, bankroll)
        result[index] = curr_episode

    median = np.median(result, axis=0)
    std = np.std(result, axis=0)
    list_array.append(median+std)
    list_array.append(median)
    list_array.append(median-std)

    plot("Fig5-1000 Episodes With Bankroll with Median", "Episodes", "Winnings", list_array, ["Median-Std","Median","Median+Std"], "Fig-5")




if __name__ == "__main__":  		  	   		  		 		  		  		    	 		 		   		 		  
    test_code()  		  	   		  		 		  		  		    	 		 		   		 		  
