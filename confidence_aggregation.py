from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components
import pandas as pd
import hashlib
from datetime import datetime, timedelta
import fuzzy
import re #regular expressions
import numpy as np
from Levenshtein import distance as levenshtein_distance
soundex = fuzzy.Soundex(4)

def findConfidenceLevel(first_name1, last_name1, rna_first_name1, rna_last_name1, first_name2, last_name2, rna_first_name2, rna_last_name2):
    if rna_first_name1 == rna_first_name2 and rna_last_name1 == rna_last_name2:
        return 100 
    elif rna_last_name1 == rna_last_name2 and rna_first_name1[:4] == rna_first_name2[:4]:
        return 90
    elif rna_last_name1 == rna_last_name2:
        return 85
    elif rna_last_name1[0:5] == rna_last_name2[0:5] and rna_first_name1[:4] == rna_first_name2[:4]:
        return 80
    elif soundex(last_name1) == soundex(last_name2) and soundex(first_name1) == soundex(first_name2):
        return 79
    elif soundex(rna_last_name1) == soundex(rna_last_name2) and soundex(rna_first_name1) == soundex(rna_first_name2):
        return 77
    elif rna_first_name1 == rna_first_name2 and soundex(rna_last_name1[:4]) == soundex(rna_last_name2[:4]):
        return 76
    elif rna_first_name1 == rna_first_name2:
        return 60
    else:
        return 50
    
def findConfidenceLevel2(first_name1, last_name1, rna_first_name1, rna_last_name1, first_name2, last_name2, rna_first_name2, rna_last_name2):   
    if rna_first_name1 == rna_first_name2 and rna_last_name1 == rna_last_name2:
        return 100
    elif rna_last_name1 == rna_last_name2 and rna_first_name1[:4] == rna_first_name2[:4]:
        return 90
    elif rna_last_name1 == rna_last_name2 and soundex(first_name1) == soundex(first_name2):
        return 85
    elif rna_last_name1[0:5] == rna_last_name2[0:5] and rna_first_name1[:4] == rna_first_name2[:4]:
        return 80
    elif soundex(last_name1) == soundex(last_name2) and soundex(first_name1) == soundex(first_name2):
        return 79
    elif soundex(rna_last_name1) == soundex(rna_last_name2) and soundex(rna_first_name1) == soundex(rna_first_name2):
        return 77
    elif rna_first_name1 == rna_first_name2 and soundex(rna_last_name1[:4]) == soundex(rna_last_name2[:4]):
        return 76
    elif rna_last_name1 == rna_last_name2:
        return 75
    elif rna_first_name1 == rna_first_name2:
        return 60
    else:
        return 50

def find_Levenshtein_Conf_Name(first_name1, last_name1, rna_first_name1, rna_last_name1, first_name2, last_name2, rna_first_name2, rna_last_name2):
    if rna_first_name1 == rna_first_name2 and rna_last_name1 == rna_last_name2:
        return 100
    elif rna_last_name1 == rna_last_name2 and rna_first_name1[:4] == rna_first_name2[:4]:
        return 90
    elif rna_last_name1 == rna_last_name2 and levenshtein_distance(first_name1, first_name2) < 4:
        return 85
    elif rna_last_name1[0:5] == rna_last_name2[0:5] and rna_first_name1[:4] == rna_first_name2[:4]:
        return 80
    elif levenshtein_distance(last_name1, last_name2) < 4 and levenshtein_distance(last_name1, last_name2) < 4:
        return 79
    elif levenshtein_distance(rna_last_name1, rna_last_name2) < 4 and levenshtein_distance(rna_first_name1, rna_first_name2) < 4:
        return 77
    elif rna_first_name1 == rna_first_name2 and levenshtein_distance(rna_last_name1[:4], rna_last_name2[:4]) < 4:
        return 76
    elif rna_last_name1 == rna_last_name2:
        return 75
    elif rna_first_name1 == rna_first_name2:
        return 60
    else:
        return 50

def find_Levenshtein_Conf_DOB(dob_1, dob2):
    if dob_1 == dob_2:
        return 80
    elif levenshtein_distance(dob1, dob2) == 1:
        return 66
    elif levenshtein_distance(dob1, dob2) == 2:
        return 5.7
    elif levenshtein_distance(dob1, dob2) == 3:
        return 0.02
    else:
        return 0

def find_Gender_Conf(g1, g2):
    if g1 == g2:
        return 100
    else:
        return 60

def compare_address(address1, address2):
    levenshtein_sum = 0
    min_street = min(len(address1), len(address2))
    for x in range(min(len(address1), len(address2))):
        # if we are comparing the last word compare the shortest combination
        if x == min_street - 1:
            min_word_length = min(len(address1[x]), len(address2[x]))
            temp1 = address1[x][:min_word_length]
            temp2 = address2[x][:min_word_length]
            levenshtein_distance(temp1, temp2)
        else:
            levenshtein_sum += levenshtein_distance(address1[x], address2[x])
    if levenshtein_sum == 0:
        return 0
    else:
        return min_street / levenshtein_sum

def generate_confidence_matrix(confidence_func, df, threshold):
    matrix = np.zeros((df.shape[0], df.shape[0]))
    for index1, row1 in df.iterrows():
        for index2, row2 in df.iterrows():
            conf = confidence_func(
                    row1['First Name'],
                    row1['Last Name'],
                    row1['rnaFirstName'],
                    row1['rnaLastName'],
                    row2['First Name'],
                    row2['Last Name'],
                    row2['rnaFirstName'],
                    row2['rnaLastName']
            )
            if conf > threshold:
                matrix[index1][index2] = 1
            else:
                matrix[index1][index2] = 0
    return matrix

def calculate_connected_components(adjacency_matrix):
    graph = csr_matrix(adjacency_matrix)
    return connected_components(csgraph=graph, directed=False, return_labels=True)