from __future__ import division

import numpy as np
from collections import defaultdict
from itertools import product
from sklearn.metrics import confusion_matrix


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


class ClassHierarchy(object):
    """A tree encoding of a class hierarchy, where each node has
    associated labeling functions to provide weak supervision signal.
    
    We consider tasks 0,1,...,T-1.
    Each non-root node Y_t takes on values in {0,1,...,K_t}, and the root node 
    takes on values in {1,...,K_0}. A parent node Y_t is connected to its child
    nodes Y_c, c \in {1,...,K_t}, by factors representing the implications:
        - Y_t != c ==> Y_c = 0
    The labeling functions \lambda associated with node Y are connected
    with the following three factor types:
        - Labeling propensity:     Y != 0 & \lambda != 0
        - Labeling Accuracy:       1 if Y != 0 & \lambda =  Y
                                  -1 if Y != 0 & \lambda = -Y
        - Null Labeling Accuracy:  1 if Y == 0 & \lambda == 0
                                  -1 if Y == 0 & \lambda != 0
    The input to initialize this class is:
        - L: A sparse label matrix of dimensions N x M, where N is the total
            number of data points and M is the number of LFs from all tasks.
        - task_to_lfs: A mapping from task index t -> a list of LF indices,
            representing the column indices in L corresponding to task t.
        - edges: A set of tuples (t, s) representing a directed edge from tasks
            t -> s.
        - cardinalities: A list of cardinalities of tasks 0,1,...,T-1 (not 
            counting the "abstain" value in non-root nodes).
    """
    def __init__(self, L, task_to_lfs, edges, cardinalities):
        # Note: Make sure the LF lists are sorted
        self.task_to_lfs = { 
            t : sorted(list(set(lfs))) for t, lfs in task_to_lfs.items()
        }
        self.edges = edges
        self.K = cardinalities

        # The number of tasks (note: t=0,1,...,T-1)
        self.T = len(task_to_lfs)
        # The decomposed list of label matrices from the LFs for each task
        self.Ls = self._parse_L(L)
        # The total and per-task number of LFs respectively
        self.M = L.shape[1]
        self.m = [Lt.shape[1] for Lt in self.Ls]
        
        # Initialize helper data structures for tree traversal
        self._children = defaultdict(list)
        self._parents = defaultdict(list)
        for s, t in self.edges:
            self._children[s].append(t)
            self._parents[t].append(s)

        # Ensure that this is a tree structure
        for c, parents in self._parents.items():
            self._parents[c] = list(set(parents))
            if len(self._parents[c]) > 1:
                raise ValueError('Multiple parents for node {}.'.format(c))

        # Ensure that the child nodes are sorted by index
        # Note that this means that value k of a node corresponds to child k-1
        for t, children in self._children.items():
            self._children[t] = sorted(list(set(children)))

        # Construct neighbors dictionary of sets
        self._neighbors = { 
            t : set(self._children[t] + self._parents[t]) for t in range(self.T)
        }

        # Get the ordered list of leaf task indices
        self.leaf_tasks = [t for t in range(self.T) 
            if all(e[0] != t for e in self.edges)]

        # Initialize caches for BP
        self._msg_cache = dict()

        # Intialize weight vector
        self.d = 3*self.M
        self.w = np.ones(self.d)
                
        # Creating tree -> categorical label dict
        self.leaf_to_cat_dict = self.leaf_to_categorical()

    def leaf_to_categorical(self):
        """
        Creates dictionary from (leaf_task, vote) tuples to
        categorical end labels.
        Inputs: None
        Outputs: lab_dict {(task,vote):categorical}
        """
        lab_dict = {}
        lab = 1
        for ind,task in enumerate(self.leaf_tasks):
            for ii in range(self.K[task]):
                # Adjusting vote output to account for votes in 1...Kt
                vote_output = ii+1
                lab_dict[(task,vote_output)] = lab
                lab += 1
        return lab_dict 

    def get_categorical_vote(self,leaf_task, leaf_vote):
        """
        Queries leaf-to-categorical label dict to obtain
        categorical vote analogous to a particular tree path.
        Inputs: leaf_task (index of leaf at end of tree path),
        leaf_vote (vote at leaf task, in 0...cardinality(leaf_task))
        Outputs: categorical vote (int)
        """
        return self.leaf_to_cat_dict[(leaf_task, leaf_vote)]

    def get_tree_path(self,task):
        tree_path = [task]
        while tree_path[0] != 0:
            tree_path.insert(0,self._parents[tree_path[0]][0])
        return tree_path

    def _make_dense(self,L):
        """Helper funtion to make matrix dense if not already."""
        try:
            return L.todense()
        except AttributeError:          
            return L

    def _parse_L(self, L):
        """Parse a sparse label matrix L into a list of task-specific label
        matrices [L_0,L_1...,L_{T-1}], using the mapping in self.task_to_lfs."""
        # NOTE: At some point we should definitely switch to using sparse
        # matrices throughout, and then this should change...
        L = np.copy(self._make_dense(L)).astype(int)
        return [L[:, self.task_to_lfs[t]] for t in range(self.T)]

    def get_node_value(self, p, c):
        """Gets the value of parent node t which child node i corresponds to."""
        if c not in self._children[p]:
            raise ValueError("Node {c} is not a child of node {p}.")
        return self._children[p].index(c) + 1

    def _clear_msg_cache(self):
        """Clear message cache."""
        self._msg_cache = dict()

    def w_labs(self, t):
        """Get the vector of LF labeling prop. weights for task Y_t != 0."""
        s = sum(self.m[:t])
        return self.w[s : s + self.m[t]]

    def w_accs(self, t):
        """Get the vector of LF accuracy weights for node Y_t != 0."""
        s = self.M + sum(self.m[:t])
        return self.w[s : s + self.m[t]]

    def w_null_accs(self, t):
        """Get the vector of LF accuracy weights for node Y_t == 0."""
        s = 2*self.M + sum(self.m[:t])
        return self.w[s : s + self.m[t]]

    def LF_label_props(self, t):
        """Get the vector of LF labeling propensities for task Y_t != 0."""
        x = np.exp(self.w_accs(t)) + np.exp(-self.w_accs(t))
        return (np.exp(self.w_labs(t)) * x) / (np.exp(self.w_labs(t)) * x + 1)

    def LF_accs(self, t):
        """Get the vector of LF accuracies for node Y_t != 0."""
        return sigmoid(2 * self.w_accs(t))

    def LF_null_accs(self, t):
        """Get the vector of LF accuracies for node Y_t != 0."""
        return sigmoid(2 * self.w_null_accs(t))

    def _factor_accs(self, Lt, t, y):
        """Labeling accuracy factors:
            h^{acc}(\lambda, Y) = 1{\lambda == Y, Y != 0}
                                - 1{\lambda != Y, Y != 0, \lambda != 0}
                                + 1{\lambda == Y, Y == 0}
                                - 1{\lambda != Y, Y == 0}
        """
        if y > 0:
            h = np.dot(np.where(Lt == 0, 0, np.where(Lt == y, 1, -1)), self.w_accs(t))
        else:
            
            # Handle special case of root node which has no null value here
            if t == 0:
                return np.zeros(Lt.shape[0])
            else:
                h = np.dot(np.where(Lt == 0, 1, -1), self.w_null_accs(t))
        return np.exp(h)

    def _msg_local(self, Lt, t):
        """Messages from the LFs of node Y_t in to label variable Y_t,
        conditioned on observed LF labels.
        Returns a K_t x N table with rows representing y_t = [0,1,...,K_{t-1}].
        """
        cache_key ='LOCAL:{}'.format(t)
        if cache_key not in self._msg_cache:
            self._msg_cache[cache_key] = np.vstack([
                self._factor_accs(Lt, t, y) for y in range(self.K[t]+1)
            ])
        return self._msg_cache[cache_key]

    def _factor_edge(self, p, c, y_p, y_c):
        """Hierarchy implication factors:
            h^{edge}(Y_p, Y_c) = 1{Y_p != index(Y_c), Y_c != 0}
                               + 1{Y-p == index(Y_c), Y_c == 0}
        """
        # Ensure that p is parent to child c; assume desc. ordering of index
        if p > c:
            return self._factor_edge(c, p, y_c, y_p)
        if (y_p != self.get_node_value(p, c) and y_c != 0) \
            or (y_p == self.get_node_value(p, c) and y_c == 0):
            return 0.0
        else:
            return 1.0

    def _msg_edge(self, Ls, s, t):
        """Message from Y_s -> Y_t, conditioned on observed LF labels.
        Returns a K_t x N table with rows representing y_t = [0,1, ...,K_{t-1}].
        """
        N = Ls[0].shape[0]
        if (s,t) not in self.edges and (t,s) not in self.edges:
            raise ValueError('({}, {}) not in edge set.'.format(s,t))

        cache_key = 'EDGE:{}->{}'.format(s,t)
        if cache_key not in self._msg_cache:
            msg = np.zeros((self.K[t]+1, N))

            # Construct message from Y_s to the joint Y_s - Y_t factor
            # This is the product of all messages in to Y_s, setting off
            # recursive computation
            msg_s = self._msg_local(Ls[s], s)
            
            for n_s in self._neighbors[s] - set([t]):
                msg_s *= self._msg_edge(Ls, n_s, s)

            # Next, compute the message from the joint Y_s - Y_t factor to Y_t
            # We take the product of msg_s with the Y_s - Y_t factor function,
            # marginalizing out y_s
            for y_s in range(self.K[s] + 1):
                for y_t in range(self.K[t] + 1):
                    msg[y_t] += self._factor_edge(s, t, y_s, y_t) * msg_s[y_s]
            self._msg_cache[cache_key] = msg
        return self._msg_cache[cache_key]

    def conditional_probs(self, Ls, t, clear_cache=True):
        """Compute the conditional marginal probabilities $P(y_t | \lambda)$
        for all data points using belief propagation over the tree.
        
        Input: a list of label matrices, L, which must have the same LFs and
        graph structure as self.Ls, and a node index of interest t.
        Returns: a K_t x N table, with rows representing values of 
        y_t = [0,1,...,K_{t-1}].
        Note: By default clears the message cache ==> everything is re-computed.
        """
        if clear_cache:
            self._clear_msg_cache()

        # Messages in from LFs to Y_t
        # NOTE: Need to copy the value to prevent overwriting the cache!
        p = np.copy(self._msg_local(Ls[t], t))

        # Messages in from other nodes
        for n_t in self._neighbors[t]:
            p *= self._msg_edge(Ls, n_t, t)

        # Normalize the probabilities and return cond. prob. table
        return p / p.sum(axis=0)

    def _prior(self, t):
        """Computes P(Y_t != 0), assume prior is uniform over the tree."""
        prob = 1.0
        p = t
        while p != 0:
            p = self._parents[p][0]
            # Probability that, given Y_p != 0, the right sub-tree was chosen
            prob *= 1 / self.K[p]
        return prob

    def _grad(self):
        """Compute the gradient. For each factor weight, this is the difference
        between the expected factor value and the expected factor value
        conditioned on the observed LF labels."""
        grad = np.zeros(self.d)
        
        # Clear message cache so all conditional probabilities are re-computed
        # THIS IS IMPORTANT!
        self._clear_msg_cache()

        # LF accuracy, labeling propensity, and null accuracy factors
        N = self.Ls[0].shape[0]
        gi = 0
        for t in range(self.T):
            L = self.Ls[t]
            beta = self.LF_label_props(t)
            alpha = self.LF_accs(t)
            alpha_null = self.LF_null_accs(t)
            cprobs = self.conditional_probs(self.Ls, t, clear_cache=False)
            for j in range(self.m[t]):

                # Labeling propensity factors
                # This factor type represents the propensity to label Y != 0
                # h^{lab}(\lambda, Y) = 1{\lambda != 0, Y != 0}
                E_lab = self._prior(t) * beta[j]
                E_lab_cond = np.where(L[:,j] != 0, 1, 0) * (1 - cprobs[0])
                grad[gi] = E_lab - np.sum(E_lab_cond) / N

                # Labeling accuracy factors
                # This factor type represents the accuracy given Y != 0
                # h^{acc}(\lambda, Y) = 1{\lambda == Y, Y != 0}
                #                      -1{\lambda != Y, Y != 0, \lambda != 0}
                E_acc = self._prior(t) * beta[j] * (2*alpha[j] - 1)
                cprobs_j = cprobs[L[:,j], range(N)]
                E_acc_cond = np.where(L[:,j] != 0, 1, 0) \
                    * (2*cprobs_j + cprobs[0] - 1)
                grad[self.M + gi] = E_acc - np.sum(E_acc_cond) / N

                # Labeling null accuracy factors
                # This factor type represents the accuracy given Y == 0
                # h^{null}(\lambda, Y) = 1{\lambda == Y, Y == 0}
                #                       -1{\lambda != Y, Y == 0}
                E_null = (1-self._prior(t)) * (2*alpha_null[j] - 1)
                E_null_cond = np.where(L[:,j] == 0, 1, -1) * cprobs[0]
                grad[2*self.M + gi] = E_null - np.sum(E_null_cond) / N

                # Increment gradient position index
                gi += 1
        return grad

    def estimation_error(self, accs, return_list=False):
        """Measure the mean parameter estimation error across all nodes, given
        a list of the T true LF accuracy vectors."""
        errs = [
            np.mean(np.abs(accs[t] - self.LF_accs(t))) for t in range(self.T)
        ]
        return errs if return_list else np.mean(errs)

    def train(self, n_steps=500, step_size=0.1, print_at=100, accs=None, l2=0.0,
        random_init=False):
        """Train the generative labeling model."""
        # Initialize weight vector with some random noise to break symmetry
        self.w = np.ones(self.d)
        if random_init:
            self.w += 0.01 * (np.random.rand(self.d) - 0.5)

        # Run SGD
        for step in range(n_steps):
            g = self._grad()

            # Optionally enforce prior on the LF accs through L2 regularization
            if l2 > 0:
                wp = np.zeros(self.d)
                wp[self.M:2*self.M] = self.w[self.M:2*self.M] - 1.0
                wp[2*self.M:3*self.M] = self.w[2*self.M:3*self.M] - 1.0
                g += 2 * l2 * wp

            # Print step and other easily computable stats
            if print_at is not None and step % print_at == 0:
                msg = 'Step {}: Gradient norm = {:0.5f}'.format(step, np.linalg.norm(g))
                
                # If true LF accuracies are provided (e.g. with synthetic data),
                # compute average difference across tasks
                if accs is not None:
                    err = self.estimation_error(accs)
                    msg += ', avg. difference in accs: {:0.5f}'.format(err)
                print(msg)

            # Take a gradient step
            self.w -= step_size * g
        if print_at > 0:
            print('Training completed.')

    def grid_search_train(self, L_dev, Y_dev, search_space, score_metric='acc',
        **kwargs):
        """Perform grid search over hyperparameters, using dev set."""
        print('Grid search over {}:'.format(search_space))
        score_opt = 0.0
        w_opt = self.w
        hp_kwargs_opt = {}
        for hps in product(*search_space.values()):
            hp_kwargs = dict(zip(search_space.keys(), hps))

            print('>>> Training for {}:'.format(hp_kwargs))
            # HACK
            temp = {}
            temp.update(hp_kwargs)
            temp.update(kwargs)
            # HACK
            self.train(**temp)

            # Get score on dev set; if best yet, save model params
            if score_metric == 'f1':
                score = self.f1_score(L_dev, Y_dev)[-1]
            else:
                score = self.accuracy(L_dev, Y_dev)
            if score > score_opt:
                score_opt = score
                w_opt = self.w
                hp_kwargs_opt = hp_kwargs

        print('Restoring model for {}.'.format(hp_kwargs_opt))
        self.w = w_opt

    def task_predictions(self, L, t):
        """Outputs an N-dim array of (integer) label predictions for Y_t,
        given sparse label matrix L."""
        return self.conditional_probs(self._parse_L(L), t).argmax(axis=0)

    def task_accuracy(self, L, t, Yt):
        """Computes the accuracy of label predictions of the model for Y_t,
        given label matrix L and true labels (for task t) Yt."""
        return np.where(self.task_predictions(L, t) == Yt, 1, 0).sum() \
            / Yt.shape[0]

    def predictions(self, L):
        """Outputs an N-dim array of (integer) label predictions for Y, i.e. 
        in the combined leaf-level classification space.
        Specifically, we consider the label set defined by enumerating over all
        of the (non-null) leaf-level task outputs, in task index order, and
        make a single prediction per data point in this space.
        Ex: A three-node tree with binary nodes encodes a four-class problem.
        Let t=0 be the root node and t=1,2 the leaf nodes. Then we map to the
        combined leaf-level classification space as follows:
            - Y_1 = 1 --> 1
            - Y_1 = 2 --> 2
            - Y_2 = 1 --> 3
            - Y_2 = 2 --> 4
        """
        # Note: This is taking the argmax across all the (non-null) *marginal*
        # conditional probabilities P(Y_t|\lxo)--this is a bit of a hack, as
        # properly we'd compute the full joint conditional probs... but should
        # be roughly okay for now.
        return np.vstack([self.conditional_probs(self._parse_L(L), t)[1:] 
            for t in self.leaf_tasks]).argmax(axis=0) + 1

    def accuracy(self, L, Y):
        """Get accuracy in the combined leaf-level classification space (see
        self.predictions above)."""
        return np.where(self.predictions(L) == Y, 1, 0).sum() / Y.shape[0]

    def f1_score(self, L, Y):
        """Get F1 score assuming 1 = -1, 2 = 1."""
        pred = self.predictions(L)

        pred_pos = np.where(pred == 2, 1, 0)
        true_pos = np.where(Y == 2, 1, 0) 
        
        # Precision
        prec = np.sum(pred_pos * true_pos) / pred_pos.sum() if pred_pos.sum() else 0.0

        # Recall
        rec = np.sum(pred_pos * true_pos) / true_pos.sum() if true_pos.sum() else 0.0

        # F1 score
        f1 = (2 * prec * rec) / (prec + rec) if (prec and rec) else 0.0
            
        return prec, rec, f1

    def confusion(self, L, Y):
        """Get confusion matrix for combined leaf-level clasification space."""
        return confusion_matrix(Y, self.predictions(L))