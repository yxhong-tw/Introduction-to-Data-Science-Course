import sklearn.metrics
from sklearn import datasets
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import math
import numpy as np
import pandas as pd


class Node:
    "Decision tree node"
    def __init__(self, entropy, num_samples, num_samples_per_class, predicted_class, num_errors, alpha = float("inf")):
        self.entropy = entropy # the entropy of current node
        self.num_samples = num_samples
        self.num_samples_per_class = num_samples_per_class
        self.predicted_class = predicted_class # the majority class of the split group
        self.feature_index = 0 # the feature index we used to split the node
        self.threshold = 0 # for binary split
        self.left = None # left child node
        self.right = None # right child node
        self.num_errors = num_errors # error after cut
        self.alpha = alpha # each node alpha


class DecisionTreeClassifier:    
    def __init__(self, max_depth = 4):
        self.max_depth = max_depth
    def _entropy(self, sample_y, n_classes):
        # TODO: calculate the entropy of sample_y and return it
        # sample_y represent the label of node
        # entropy = -sum(pi * log2(pi))
        entropy = 0

        # My code start
        p = 0
        for i in range(sample_y.size):
            if sample_y[i] == 1:
                p += 1

        n = sample_y.size - p

        if p == 0:
            entropy = -((n / sample_y.size) * math.log2(n / sample_y.size))
        elif n == 0:
            entropy = -((p / sample_y.size) * math.log2(p / sample_y.size))
        else:
            entropy = -((p / sample_y.size) * math.log2(p / sample_y.size)) - ((n / sample_y.size) * math.log2(n / sample_y.size))
        # My code end

        return entropy

    def _feature_split(self, X, y, n_classes):
        # Returns:
        #  best_idx: Index of the feature for best split, or None if no split is found.
        #  best_thr: Threshold to use for the split, or None if no split is found.
        m = y.size
        if m <= 1:
            return None, None

        # Entropy of current node.

        best_criterion = self._entropy(y, n_classes)

        best_idx, best_thr = None, None
        # TODO: find the best split, loop through all the features, and consider all the
        # midpoints between adjacent training samples as possible thresholds. 
        # Compute the Entropy impurity of the split generated by that particular feature/threshold
        # pair, and return the pair with smallest impurity.

        # My code start
        best_gain = 0

        for i in range(np.size(X, 1)):
            for j in range(np.size(X, 0)):
                left, right = [], []
                for k in range(np.size(X, 0)):
                    if X[k][i] <= X[j][i]:
                        left.append(y[k])
                    else:
                        right.append(y[k])

                left = np.array(left)
                right = np.array(right)

                if left.size == 0:
                    gain = self._entropy(right, n_classes)
                elif right.size == 0:
                    gain = self._entropy(left, n_classes)
                else:
                    gain = (((left.size/(right.size+left.size))*self._entropy(left, n_classes)) + ((right.size/(right.size+left.size))*self._entropy(right, n_classes)))
            
                if best_gain < (best_criterion - gain):
                    best_gain = (best_criterion - gain)
                    best_idx = i
                    best_thr = X[j][i]
        # My code end

        return best_idx, best_thr
    def _build_tree(self, X, y, depth=0):
        num_samples_per_class = [np.sum(y == i) for i in range(self.n_classes_)]
        predicted_class = np.argmax(num_samples_per_class)
        correct_label_num = num_samples_per_class[predicted_class]
        num_errors = y.size - correct_label_num
        node = Node(
            entropy = self._entropy(y, self.n_classes_),
            num_samples = y.size,
            num_samples_per_class = num_samples_per_class,
            predicted_class = predicted_class,
            num_errors = num_errors
        )

        if depth < self.max_depth:
            idx, thr = self._feature_split(X, y, self.n_classes_)
            if idx is not None:
                # TODO: Split the tree recursively according index and threshold until maximum depth is reached.

                # My code start
                node.feature_index = idx
                node.threshold = thr

                left_X, left_y, right_X, right_y = [], [], [], []
                for i in range(np.size(X, 0)):
                    if X[i][idx] <= thr:
                        left_X.append(X[i])
                        left_y.append(y[i])
                    else:
                        right_X.append(X[i])
                        right_y.append(y[i])

                left_X = np.array(left_X)
                left_y = np.array(left_y)
                right_X = np.array(right_X)
                right_y = np.array(right_y)

                depth += 1
                node.left = self._build_tree(left_X, left_y, depth)
                node.right = self._build_tree(right_X, right_y, depth)
                # My code end

                pass
        return node

    def fit(self,X,Y):
        # TODO
        # Fits to the given training data

        # My code start
        self.n_classes_ = 2
        self.tree_ = self._build_tree(X, Y)
        # My code end

        pass

    def predict(self,X):
        pred = []
        #TODO: predict the label of data

        # My code start
        for i in range(np.size(X, 0)):
            temp_tree = self.tree_
            while(True):
                if temp_tree.left == None and temp_tree.right == None:
                    pred.append(temp_tree.predicted_class)
                    break
                else:
                    if X[i][temp_tree.feature_index] <= temp_tree.threshold:
                        temp_tree = temp_tree.left
                    else:
                        temp_tree = temp_tree.right
        # My code end

        return pred

    def _find_leaves(self, root):
        #TODO
        ## find each node child leaves number

        # My code start
        leaves_number = 0
        queue = []
        queue.append(root)

        while(True):
            if len(queue) == 0:
                break
            else:
                temp_root = queue[0]
                queue.pop(0)

                if temp_root.left != None:
                    queue.append(temp_root.left)

                if temp_root.right != None:
                    queue.append(temp_root.right)

                if temp_root.left == None and temp_root.right == None:
                    leaves_number += 1

        return leaves_number
        # My code end

        pass

    def _error_before_cut(self, root):
        # TODO
        ## return error before post-pruning

        # My code start
        errors_before_cut_number = 0
        queue = []
        queue.append(root)

        while(True):
            if len(queue) == 0:
                break
            else:
                temp_root = queue[0]
                queue.pop(0)

                if temp_root.left != None:
                    queue.append(temp_root.left)

                if temp_root.right != None:
                    queue.append(temp_root.right)

                if temp_root.left == None and temp_root.right == None:
                    errors_before_cut_number += temp_root.num_errors

        return errors_before_cut_number
        # My code end

        pass

    def _compute_alpha(self, root):
        # TODO
        ## Compute each node alpha
        # alpha = (error after cut - error before cut) / (leaves been cut - 1)

        # My code start
        queue = []
        queue.append(root)

        while(True):
            if len(queue) == 0:
                break
            else:
                temp_node = queue[0]
                queue.pop(0)

                if temp_node.left != None:
                    queue.append(temp_node.left)

                if temp_node.right != None:
                    queue.append(temp_node.right)

                if temp_node.left != None and temp_node.right:
                    temp_node.alpha = ((temp_node.num_errors - self._error_before_cut(temp_node)) / (self._find_leaves(temp_node) - 1))
                else:
                    temp_node.alpha = float("inf")
        # My code end

        pass
    
    def _find_min_alpha(self, root):
        MinAlpha = float("inf")
        # TODO
        ## Search the Decision tree which have minimum alpha's node

        # My code start
        ret = []
        queue = []
        queue.append(root)

        while(True):
            if len(queue) == 0:
                break
            else:
                temp_node = queue[0]
                queue.pop(0)

                if temp_node.left != None:
                    queue.append(temp_node.left)
                if temp_node.right != None:
                    queue.append(temp_node.right)
                    
                if temp_node.alpha < MinAlpha:
                    ret.append(temp_node)
                    MinAlpha = temp_node.alpha

        return ret[len(ret) - 1]
        # My code end

        pass

    def _prune(self):
        self._compute_alpha(self.tree_)
        cut_node = self._find_min_alpha(self.tree_)
        # TODO
        ## prune the decision tree with minimum alpha node

        # My code start
        cut_node.left = None
        cut_node.right = None
        # My code end

        pass

def load_train_test_data(test_ratio = .3, random_state = 1):
    df = pd.read_csv('.\heart_dataset.csv')
    # df = pd.read_csv('.\Exercise_2\heart_dataset.csv')  # Change file directory
    X = df.drop(columns = ['target'])
    X = np.array(X.values)
    y = df['target']
    y = np.array(y.values)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size = test_ratio, random_state = random_state, stratify = y)
    return X_train, X_test, y_train, y_test

def accuracy_report(X_train_scale, y_train, X_test_scale, y_test, max_depth = 7):
    tree = DecisionTreeClassifier(max_depth = max_depth)
    tree.fit(X_train_scale, y_train)
    pred = tree.predict(X_train_scale)

    print(" tree train accuracy: %f" 
        % (sklearn.metrics.accuracy_score(y_train, pred)))
    pred = tree.predict(X_test_scale)
    print(" tree test accuracy: %f" 
        % (sklearn.metrics.accuracy_score(y_test, pred)))
    
    for i in range(10):
        print("=============Cut=============")
        tree._prune()
        pred = tree.predict(X_train_scale)
        print(" tree train accuracy: %f" 
            % (sklearn.metrics.accuracy_score(y_train, pred )))
        pred = tree.predict(X_test_scale)
        print(" tree test accuracy: %f" 
            % (sklearn.metrics.accuracy_score(y_test, pred )))

def main():
    X_train, X_test, y_train, y_test = load_train_test_data(test_ratio = .3, random_state = 1)
    accuracy_report(X_train, y_train, X_test, y_test, max_depth = 8)
if __name__ == "__main__":
    main()