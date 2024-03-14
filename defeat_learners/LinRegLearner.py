import numpy as np

class LinRegLearner(object):

    def __init__(self, verbose=False):
        pass

    def author(self):
        return 'svaja6'

    def add_evidence(self, dataX, dataY):
        newdataX = np.ones([dataX.shape[0], dataX.shape[1] + 1])
        newdataX[:, 0:dataX.shape[1]] = dataX
        self.model_coefs, _, _, _ = np.linalg.lstsq(newdataX, dataY, rcond=None)

    def query(self, points):
        return (self.model_coefs[:-1] * points).sum(axis=1) + self.model_coefs[-1]


