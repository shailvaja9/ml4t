import numpy as np
import random

class RTLearner(object):

    def __init__(self, leaf_size=1, verbose=False, seed=None):
        self.leaf_size = leaf_size
        self.verbose = verbose

        if seed is not   None:
            random.seed(seed)
        self.tree = None
    def author(self):
        return 'svaja6'

    def add_evidence(self, dataX, dataY):
        self.tree = self.build_tree(dataX, dataY)
        if self.verbose:
            print("RTLearner: Tree built with shape:", self.tree.shape)


    def query(self, points):
        predictions = np.array([self.get_prediction(point) for point in points])
        return predictions

    def get_prediction(self, point, node=0):
        while ~np.isnan(self.tree[node][0]):
            split_value = point[int(self.tree[node][0])]
            if split_value <= self.tree[node][1]:
                node += int(self.tree[node][2])
            else:
                node += int(self.tree[node][3])
        return self.tree[node][1]

    def build_tree(self, dataX, dataY):
        if dataX.shape[0] <= self.leaf_size:
            return np.asarray([np.nan, np.mean(dataY), np.nan, np.nan])

        if np.all(np.isclose(dataY, dataY[0])):
            return np.asarray([np.nan, dataY[0], np.nan, np.nan])

        feature_index = random.randrange(dataX.shape[1])
        point1, point2 = random.sample(range(dataX.shape[0]), 2)
        split_value = (dataX[point1][feature_index] + dataX[point2][feature_index]) / 2

        left_dataset = dataX[:, feature_index] <= split_value
        if np.all(np.isclose(left_dataset, left_dataset[0])):
            return np.asarray([np.nan, np.mean(dataY), np.nan, np.nan])

        right_dataset = np.logical_not(left_dataset)
        left_tree = self.build_tree(dataX[left_dataset], dataY[left_dataset])
        right_tree = self.build_tree(dataX[right_dataset], dataY[right_dataset])

        if left_tree.ndim == 1:
            root = np.asarray([feature_index, split_value, 1, 2])
        else:
            root = np.asarray([feature_index, split_value, 1, left_tree.shape[0] + 1])

        return np.row_stack((root, left_tree, right_tree))


