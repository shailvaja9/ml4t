import numpy as np

class BagLearner:
    def __init__(self, learner, bags=1, kwargs={}, boost=False, verbose=False):
        self.boost = boost
        self.verbose = verbose
        self.learners = [learner(**kwargs) for _ in range(bags)]

    def author(self):
        return 'svaja6'

    def add_evidence(self, dataX, dataY):
        if self.verbose:
            print("Bag Learner: adding evidence")
        for learner in self.learners:
            indices = np.random.choice(len(dataX), len(dataX), replace=True)
            bag_x = dataX[indices]
            bag_y = dataY[indices]
            learner.add_evidence(bag_x, bag_y)

    def query(self, points):
        predictions = [learner.query(points) for learner in self.learners]
        return np.mean(predictions, axis=0)


