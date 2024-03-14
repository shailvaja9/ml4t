import numpy as np

class LinRegLearner(object):

    def __init__(self, verbose=False):
        self.verbose = verbose

    def author(self):
        return 'svaja6'

    def add_evidence(self, dataX, dataY, verbose=False):
        if self.verbose:

            print(f"LinRegLearner calculation beginining")
        newdataX = np.ones([dataX.shape[0], dataX.shape[1] + 1])
        newdataX[:, 0:dataX.shape[1]] = dataX
        self.model_coefs, _, _, _ = np.linalg.lstsq(newdataX, dataY, rcond=None)

    def query(self, points):
        newpoints = np.ones([points.shape[0], points.shape[1] + 1])
        newpoints[:, 0:points.shape[1]] = points
        return np.dot(newpoints, self.model_coefs)


