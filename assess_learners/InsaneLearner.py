import BagLearner as bl
import LinRegLearner as lrl


class InsaneLearner(object):

    def __init__(self, verbose=False):
        self.learners = []
        self.verbose = verbose
        for _ in range(20):
            bag_learner = bl.BagLearner(learner=lrl.LinRegLearner, kwargs={}, bags=20, boost=False, verbose=False)
            self.learners.append(bag_learner)

    def author(self):
        return 'svaja6'

    def add_evidence(self, dataX, dataY):
        if self.verbose:
            print("InsaneLearner: initiated adding evidence")
        for learner in self.learners:
            learner.add_evidence(dataX, dataY)

    def query(self, points):
        out = []
        for learner in self.learners:
            prediction = learner.query(points)
            out.append(prediction)
        return sum(out) / len(out)



