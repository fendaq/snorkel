import numpy as np

from snorkel.learning.classifier import Classifier

class MajorityVoter(Classifier):
    """Simple Classifier using majority vote from an AnnotationMatrix."""
    def marginals(self, X, **kwargs):
        return np.where(np.ravel(np.sum(X, axis=1)) <= 0, 0.0, 1.0)

class SoftMajorityVoter(Classifier):
    """Simple Classifier using 'soft' majority vote from an AnnotationMatrix."""
    def marginals(self, X, **kwargs):
        net_votes = np.sum(X, axis=1)
        num_votes = np.sum(abs(X), axis=1)
        marginals = np.ravel(np.divide(net_votes + num_votes, 2.0 * num_votes))
        marginals[np.where(np.isnan(marginals))] = 0.5
        return marginals