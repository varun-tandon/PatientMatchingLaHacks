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
    return conf.generate_confidence_matrix(conf.findConfidenceLevel, df, 80, df.shape[0])

def generate_heuristic_based_votes(df):
    return conf.generate_confidence_matrix(conf.compare_patients, df, 80, df.shape[0])

def generate_ensemble_votes(df):
    
    
    cluster_votes = generate_cluster_votes(df)
    par_hash_votes = generate_par_hash_votes(df)
    full_hash_votes = generate_full_hash_votes(df)
    heuristic_votes =  generate_heuristic_based_votes(df)
    
    heuristic_votes = np.multiply(heuristic_votes, 2)
    
    sum = np.add(heuristic_votes, full_hash_votes)
    sum = np.add(sum, par_hash_votes)
    sum = np.add(sum, cluster_votes)
    
    for i in range(sum.shape[0]):
        for j in range(sum.shape[1]):
            if sum[i,j] > 2:
                sum[i,j] = True
            else:
                sum[i,j] = False


    
    
#
#    majority_vote = cluster_votes
#
#    for i in range(majority_vote.shape[0]):
#        for j in range(majority_vote.shape[1]):
#            if cluster_votes[i,j] == par_hash_votes[i,j] and cluster_votes[i,j] == full_hash_votes[i,j]:
#                majority_vote[i,j] = True
#
##    majority_vote = np.equal(cluster_votes, par_hash_votes)
##    majority_vote = np.equal(majority_vote, full_hash_votes)
#
#    print(cluster_votes)
#    print(par_hash_votes)
#    print(full_hash_votes)
#    print(majority_vote)
#    input()
#
#    heuristic_votes =  generate_heuristic_based_votes(df)
#
#    for i in range(majority_vote.shape[0]):
#        for j in range(majority_vote.shape[1]):
#            if majority_vote[i,j]:
#                heuristic_votes[i,j] = par_hash_votes[i,j]

    return sum






df_patient = dc.load_and_clean_data('Patient Matching Data.csv')
generate_cluster_votes(df_patient)
