import pandas as pd
import numpy as np
import data_cleaning as dc
import clustering as clust
import confidence_aggregation as conf
import evaluation

def convert_labels_to_matrix(labels, vote_matrix, df):
    for index1, row1 in df.iterrows():
        for index2, row2 in df.iterrows():
            if labels[index1] == labels[index2]:
                vote_matrix[index1][index2] = 1
            else:
                vote_matrix[index1][index2] = 0

def convert_partial_hash_to_matrix(vote_matrix, df):
    for index1, row1 in df.iterrows():
        for index2, row2 in df.iterrows():
            if row1['partial_name_hash'] == row2['partial_name_hash']:
                vote_matrix[index1][index2] = 1
            else:
                vote_matrix[index1][index2] = 0

def convert_full_hash_to_matrix(vote_matrix, df):
    for index1, row1 in df.iterrows():
        for index2, row2 in df.iterrows():
            if row1['full_name_hash'] == row2['full_name_hash']:
                vote_matrix[index1][index2] = 1
            else:
                vote_matrix[index1][index2] = 0

def generate_cluster_votes(df):
    vote_matrix = np.zeros((df.shape[0], df.shape[0]))
    labels = clust.perform_clustering(df)
    convert_labels_to_matrix(labels, vote_matrix, df)
    return vote_matrix

def generate_par_hash_votes(df):
    vote_matrix = np.zeros((df.shape[0], df.shape[0]))
    convert_partial_hash_to_matrix(vote_matrix, df)
    return vote_matrix

def generate_full_hash_votes(df):
    vote_matrix = np.zeros((df.shape[0], df.shape[0]))
    convert_full_hash_to_matrix(vote_matrix, df)
    return vote_matrix

def generate_default_confidence_based_votes(df):
    return conf.generate_confidence_matrix(conf.findConfidenceLevel, df, 80)

df_patient = dc.load_and_clean_data('Patient Matching Data.csv')
generate_cluster_votes(df_patient)