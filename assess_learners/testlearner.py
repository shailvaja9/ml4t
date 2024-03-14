""""""  		  	   		  		 		  		  		    	 		 		   		 		  
"""  		  	   		  		 		  		  		    	 		 		   		 		  
Test a learner.  (c) 2015 Tucker Balch  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
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
"""  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
import numpy as np  		   	  			  	 		  		  		    	 		 		   		 		  
import math 	  			  	 		  		  		    	 		 		   		 		  
import LinRegLearner as lrl
import DTLearner as dtl
import RTLearner as rtl
import BagLearner as bl
import InsaneLearner as il
import matplotlib.pyplot as plt
import time
import sys
import os

def experiment_1(train_x, train_y, test_x, test_y):
    max_leaf_size = 50
    in_sample_rsmes = []
    out_sample_rsmes = []

    for each_leaf_size in range(1, max_leaf_size + 1):
        learner = dtl.DTLearner(leaf_size = each_leaf_size,verbose = False)
        learner.add_evidence(train_x, train_y)


        in_sample_prediction_Y = learner.query(train_x)
        in_sample_rmse = math.sqrt(((train_y - in_sample_prediction_Y) ** 2).sum()/train_y.shape[0])


        out_sample_prediction_Y = learner.query(test_x)
        out_sample_rsme = math.sqrt(((test_y - out_sample_prediction_Y) ** 2).sum()/test_y.shape[0])

        in_sample_rsmes.append(in_sample_rmse)
        out_sample_rsmes.append(out_sample_rsme)



    xi = range(1, max_leaf_size + 1)
    plt.plot(xi, in_sample_rsmes, label = "in-sample")
    plt.plot(xi, out_sample_rsmes, label = "out-sample")

    plt.title("Figure 1 - DTLearner-Leaf Size vs Overfitting")
    plt.xlabel("Leaf Size")
    plt.ylabel("RMSE")

    plt.grid()
    plt.legend()
    #my_path = "/usr/src/app/assess_learners/"
    my_path = os.path.dirname(__file__)
    filename = os.path.join(my_path, "images", "fig1.png")
    plt.savefig(filename)

    plt.clf()

def experiment_2(train_x, train_y, test_x, test_y):
    max_leaf_size = 50
    bag_size = 20
    in_sample_rsmes = []
    out_sample_rsmes = []

    for each_leaf_size in range(1, max_leaf_size + 1):
        if each_leaf_size % 25 == 0:
            print("Progress:" + str(int(100*each_leaf_size/max_leaf_size)) + "%")
        learner = bl.BagLearner(learner=dtl.DTLearner,kwargs={"leaf_size":each_leaf_size},bags=bag_size,boost=False,verbose=False)
        learner.add_evidence(train_x, train_y)


        in_sample_prediction_Y = learner.query(train_x)
        in_sample_rsme = math.sqrt(((train_y - in_sample_prediction_Y) ** 2).sum()/train_y.shape[0])


        out_sample_prediction_Y = learner.query(test_x)
        out_sample_rmse = math.sqrt(((test_y - out_sample_prediction_Y) ** 2).sum()/test_y.shape[0])

        in_sample_rsmes.append(in_sample_rsme)
        out_sample_rsmes.append(out_sample_rmse)
    
    xi = range(1, max_leaf_size + 1)
    plt.plot(xi, in_sample_rsmes, label = "in-sample")
    plt.plot(xi, out_sample_rsmes, label = "out-sample")
    
    plt.title("Figure 2 - DTLearner-Leaf Size vs Overfitting in BagLearner with " + str(bag_size) + " bags")
    plt.xlabel("Leaf Size")
    plt.ylabel("RMSE")
    plt.xticks(np.insert(np.arange(5, max_leaf_size + 1, step=5),0,1))
    plt.grid()
    plt.legend()
    #my_path = "/usr/src/app/assess_learners/"
    my_path = os.path.dirname(__file__)
    filename = os.path.join(my_path, "images", "fig2.png")
    plt.savefig(filename)

    plt.clf()


def experiment_3_1(train_x, train_y):

    max_trainning_size = train_x.shape[0]
    running_time_dt = []
    running_time_rt = []
    #print("Max training size" , max_trainning_size)

    for training_size in range(1, max_trainning_size + 1,5):
        curr_train_x = train_x[:training_size]
        curr_train_y = train_y[:training_size]

        learner = dtl.DTLearner(leaf_size = 1,verbose = False)
        start = time.time()
        learner.add_evidence(curr_train_x, curr_train_y)
        end = time.time()
        running_time = end - start
        running_time_dt.append(running_time)

        learner = rtl.RTLearner(leaf_size = 1,verbose = False)
        start = time.time()
        learner.add_evidence(curr_train_x, curr_train_y)
        end = time.time()
        running_time = end - start
        running_time_rt.append(running_time)

    print(running_time_dt)
    print(running_time_rt)
    my_path = os.path.dirname(__file__)
    xi = range(1, max_trainning_size + 1, 5)

    plt.plot(xi, running_time_dt, label = "DecisionTree")
    plt.plot(xi, running_time_rt, label = "RandomTree")
    plt.title("Figure 3 - Training time comparison for Decision Tree and Random Tree")
    plt.xlabel("Training Size")
    plt.ylabel("Time")
    plt.xticks(np.arange(1, max_trainning_size + 1, step=5))
    plt.grid()
    plt.legend()
    #my_path = "/usr/src/app/assess_learners/"
    filename = os.path.join(my_path, "images", "fig3.png")
    plt.savefig(filename)
    #print(filename)


    plt.clf()

    
    


def experiment_3_2(train_x, train_y, test_x, test_y):
    max_leaf_size = 30
    out_sample_mae_dt = []
    out_sample_mae_rt = []
        
    for each_leaf_size in range(1, max_leaf_size + 1):
        learner = dtl.DTLearner(leaf_size = each_leaf_size,verbose = False)
        learner.add_evidence(train_x, train_y)
        out_sample_prediction_Y = learner.query(test_x)
        out_sample_mae = np.mean(np.abs((np.asarray(test_y) - np.asarray(out_sample_prediction_Y))))
        out_sample_mae_dt.append(out_sample_mae * 100)
    
        learner = rtl.RTLearner(leaf_size = each_leaf_size,verbose = False)
        learner.add_evidence(train_x, train_y)
        out_sample_prediction_Y = learner.query(test_x)
        out_sample_mae = np.mean(np.abs((np.asarray(test_y) - np.asarray(out_sample_prediction_Y))))
        out_sample_mae_rt.append(out_sample_mae * 100)
    


    xi = range(1, max_leaf_size + 1)
    plt.plot(xi, out_sample_mae_dt, label = "DecisionTree")
    plt.plot(xi, out_sample_mae_rt, label = "RandomTree")
    plt.title("Figure 4 - MAE Comparison DecisionTree vs RandomTree")
    plt.xlabel("Leaf Size")
    plt.ylabel("MAE")

    plt.grid()
    plt.legend()
    #my_path = "/usr/src/app/assess_learners/"
    my_path = os.path.dirname(__file__)
    filename = os.path.join(my_path, "images", "fig4.png")
    plt.savefig(filename)

    plt.clf()

if __name__ == "__main__":  		  	   		  		 		  		  		    	 		 		   		 		  
    if len(sys.argv) != 2:  		  	   		  		 		  		  		    	 		 		   		 		  
        print("Usage: python testlearner.py <filename>")  		  	   		  		 		  		  		    	 		 		   		 		  
        sys.exit(1)  		  	   		  		 		  		  		    	 		 		   		 		  
    inf = open(sys.argv[1])  		  	   		  		 		  		  		    	 		 		   		 		  
    data = np.array(  		  	   		  		 		  		  		    	 		 		   		 		  
        [list(map(str, s.strip().split(","))) for s in inf.readlines()]
    )

    if sys.argv[1] == "Data/Istanbul.csv":
        data = data[1:,1:]

    data = data.astype('float')
  		  	   		  		 		  		  		    	 		 		   		 		  

    train_rows = int(0.6 * data.shape[0])  		  	   		  		 		  		  		    	 		 		   		 		  
    test_rows = data.shape[0] - train_rows  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  

    train_x = data[:train_rows, 0:-1]  		  	   		  		 		  		  		    	 		 		   		 		  
    train_y = data[:train_rows, -1]  		  	   		  		 		  		  		    	 		 		   		 		  
    test_x = data[train_rows:, 0:-1]  		  	   		  		 		  		  		    	 		 		   		 		  
    test_y = data[train_rows:, -1]  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
    print(f"{test_x.shape}")  		  	   		  		 		  		  		    	 		 		   		 		  
    print(f"{test_y.shape}")  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  

    learner = lrl.LinRegLearner(verbose=True)
    learner.add_evidence(train_x, train_y)
    print(learner.author())  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  

    pred_y = learner.query(train_x)
    rmse = math.sqrt(((train_y - pred_y) ** 2).sum() / train_y.shape[0])  		  	   		  		 		  		  		    	 		 		   		 		  
    print()  		  	   		  		 		  		  		    	 		 		   		 		  
    print("In sample results")  		  	   		  		 		  		  		    	 		 		   		 		  
    print(f"RMSE: {rmse}")  		  	   		  		 		  		  		    	 		 		   		 		  
    c = np.corrcoef(pred_y, y=train_y)  		  	   		  		 		  		  		    	 		 		   		 		  
    print(f"corr: {c[0,1]}")  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  

    pred_y = learner.query(test_x)
    rmse = math.sqrt(((test_y - pred_y) ** 2).sum() / test_y.shape[0])  		  	   		  		 		  		  		    	 		 		   		 		  
    print()  		  	   		  		 		  		  		    	 		 		   		 		  
    print("Out of sample results")  		  	   		  		 		  		  		    	 		 		   		 		  
    print(f"RMSE: {rmse}")  		  	   		  		 		  		  		    	 		 		   		 		  
    c = np.corrcoef(pred_y, y=test_y)  		  	   		  		 		  		  		    	 		 		   		 		  
    print(f"corr: {c[0,1]}")  	
    

    experiment_1(train_x, train_y, test_x, test_y)
    experiment_2(train_x, train_y, test_x, test_y)
    experiment_3_1(train_x, train_y)
    experiment_3_2(train_x, train_y, test_x, test_y)







