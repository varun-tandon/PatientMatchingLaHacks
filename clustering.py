from sklearn.neighbors import DistanceMetric
from sklearn.cluster import AgglomerativeClustering
import numpy as np
import pandas as pd

'''
Inspiration for clustering discrete and mixed data comes from stackoverflow:
https://datascience.stackexchange.com/questions/8681/clustering-for-mixed-numeric-and-nominal-discrete-data
'''

def gower_distance(X):
    """
    This function expects a pandas dataframe as input
    The data frame is to contain the features along the columns. Based on these features a
    distance matrix will be returned which will contain the pairwise gower distance between the rows
    All variables of object type will be treated as nominal variables and the others will be treated as 
    numeric variables.
    Distance metrics used for:
    Nominal variables: Dice distance (https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient)
    Numeric variables: Manhattan distance normalized by the range of the variable (https://en.wikipedia.org/wiki/Taxicab_geometry)
    """
    individual_variable_distances = []

    for i in range(X.shape[1]):
        feature = X.iloc[:,[i]]
        if feature.dtypes[0] == np.object:
            feature_dist = DistanceMetric.get_metric('dice').pairwise(pd.get_dummies(feature))
        else:
            feature_dist = DistanceMetric.get_metric('manhattan').pairwise(feature) / np.ptp(feature.values)

        individual_variable_distances.append(feature_dist)

    return np.array(individual_variable_distances).mean(0)

def calculate_df_gower(df):
    df.fillna(0, inplace=True)
    return gower_distance(df)

def perform_clustering(df):
    X = calculate_df_gower(df)
    clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=0.8).fit(X)
    return clustering.labels_