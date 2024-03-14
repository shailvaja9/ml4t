import numpy as np

class DTLearner(object):

    def __init__(self, leaf_size = 1, verbose = False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.tree = None

    def author(self):
        return 'svaja6'

    def add_evidence(self,dataX,dataY):

        self.tree = self.build_tree(dataX, dataY)
        if self.verbose:
            print(f"DTLearner\ntree shape: {self.tree.shape}\ntree details below\n{self.tree}")



    def query(self,points):

        predictions = np.apply_along_axis(self.get_prediction, 1, points)
        return predictions

    def get_prediction(self, point, node=0):

        if np.isnan(self.tree[node, 0]):
            return self.tree[node, 1]
        feature, split_value, left, right = self.tree[node]
        if point[int(feature)] <= split_value:
            return self.get_prediction(point, node + int(left))
        else:
            return self.get_prediction(point, node + int(right))

    def get_best_feature(self, dataX, dataY):
        correlations = []
        for i in range(dataX.shape[1]):
            if np.std(dataX[:, i]) > 0:
                correlation = np.corrcoef(dataX[:, i], dataY)[0, 1]
            else:
                correlation = 0
            correlations.append(correlation)
        correlations_array = np.array(correlations)
        feature_index = np.nanargmax(np.abs(correlations_array))
        return feature_index


    def build_tree(self, dataX, dataY):
        if dataX.shape[0] <= self.leaf_size or len(np.unique(dataY)) == 1:
            return np.array([[np.nan, np.mean(dataY), np.nan, np.nan]])
        best_feature = self.get_best_feature(dataX, dataY)
        split_value = np.median(dataX[:, best_feature])
        left_dataset = dataX[:, best_feature] <= split_value
        right_dataset = dataX[:, best_feature] > split_value
        left_dataX = dataX[left_dataset]
        right_dataX = dataX[right_dataset]
        if len(left_dataX) == 0 or len(right_dataX) == 0:
            return np.array([[np.nan, np.mean(dataY), np.nan, np.nan]])
        left_tree = self.build_tree(left_dataX, dataY[left_dataset])
        right_tree = self.build_tree(right_dataX, dataY[right_dataset])
        root = np.array([[best_feature, split_value, 1, left_tree.shape[0] + 1]])
        tree = np.vstack((root, left_tree, right_tree))
        return tree


if __name__=="__main__":
    print('not implemented')
