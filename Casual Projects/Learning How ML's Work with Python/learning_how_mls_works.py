# The purpose of this project is to learn how ML algorithms works
# The crude way, no python packages(mostly)
# This was created with the purpose of using binary classification ONLY

import numpy as np
import pandas as pd

class DecisionTree:
    # The Decision Tree Structure:
    # Setting depth thresholds in order to overfit noise as the tree gets deeper
    def __init__(self, max_depth = 4, depth = 1):
        self.max_depth = max_depth
        self.depth = depth
        self.left = None
        self.right = None


    # Fit Function: Accepts the data and a string for the target attribute
    # then assigns them to a object
    def fit(self, data, target):
        if self.depth <= self.max_depth: print(f"processing at Depth: {self.depth}")
        self.data = data
        self.target = target
        self.independant = self.data.columns.tolist()
        self.independant.remove(target)
        if self.depth <= self.max_depth:
            self.__validate_data()
            self.impurity_score = self.__calculate_impurity_score(self.data[self.target])
            self.criteria, self.split_feature, self.information_gain = self.__find_best_split()
            if self.criteria is not None and self.information_gain > 0: self.__create_branches()
        else:
            print("Stopping splitting as Max depth reached")


    # Creating the inital branches and setting depth
    def __create_branches(self):
        self.left = DecisionTree(max_depth= self.max_depth,
                                  depth= self.depth + 1)
        self.right = DecisionTree(max_depth= self.max_depth,
                                  depth= self.depth + 1)
        left_row = self.data[self.data[self.split_feature] <= self.criteria]
        right_row = self.data[self.data[self.split_feature] > self.criteria]
        self.left.fit(data= left_row, target=self.target)
        self.right.fit(data= right_row, target= self.target) 


    # This calucaltes the probability of multiple classes. 
    def __calculate_impurity_score(self,data):
        if data is None or data.empty: return 0
        p_i, _ = data.value_counts().apply(lambda x: x/len(data)).tolist()
        return p_i * (1 - p_i) * 2

   
    # Given a feature, all the unique values are separated
    # For each value, a split is made in such a way the data is either <= to the value or > than the value
    def __find_best_split(self):
        best_split = {}
        for col in self.independant:
            information_gain, split = self.__find_best_split_for_column(col)
            if split is None: continue
            if not best_split or best_split["information_gain"] < information_gain:
                best_split = {"split": split,
                              "col": col,
                              "information_gain": information_gain}
        return best_split["split"], best_split["col"]


    # Then we calculate the impurity score of each branch
    def __find_best_split_for_column(self, col):
        x = self.data[col]
        unique_values = x.unique()
        if len(unique_values) == 1: return None, None
        information_gain = None
        split = None
        for val in unique_values:
            left = x <= val
            right = x > val
            left_data = self.data[left]
            right_data = self.data[right]
            left_impurity = self.__calculate_impurity_score(left_data[self.target])
            right_impurity = self.__calculate_impurity_score(right_data[self.target])
            score = self.__calculate_information_gain(left_count = len(left_data),
                                                      left_impurity = left_impurity,
                                                      right_count = len(right_data),
                                                      right_impurity = right_impurity)

            if information_gain is None or score > information_gain:
                information_gain = score
                split = val
        return information_gain, split
    
    # Calculating the information gain
    def __calculate_information_gain(self, left_count, left_impurity, right_count, right_impurity):
        return self.impurity_score - ((left_count/len(self.data) * left_impurity) + \
                                      (right_count/len(self.data) * right_impurity))


    # Predict function: iterates through the test data and returns the probability
    # based on frequency
    def predict(self, data):
        return np.array([self.__flow_data_thru_tree(row) for _, row in data.iterrows()])


    # Validating the data to make sure all data used is numerical
    def __validate_data(self):
        non_numeric_columns = self.data[self.independant].select_dtypes(include=['category', 'object', 'bool']).columns.tolist()
        if (len(set(self.independant).intersection(set(non_numeric_columns))) != 0):
            raise RuntimeError("Not all columns are numeric")

        self.data[self.target] = self.data[self.target].astype("category")
        if(len(self.data[self.target].cat.categories) != 2):
            raise RuntimeError("Implementation is only for Binary Classification")


    # Returning data (either Left or Right branch of the tree)
    def __flow_data_thru_tree(self, row):
        if self.is_leaf_node: return self.probability
        tree = self.left if row[self.split_feature] <= self.criteria else self.right
        return tree. __flow_data_thru_tree(row)

    # Checks to see if we reached a leaf in the decision tree
    @property
    def is_leaf_node(self): return self.left is None

    # Predicting probablity of the test data
    @property
    def probability(self):
        return self.data[self.target].value_counts().apply(lambda x: x/len(self.data)).tolist()
