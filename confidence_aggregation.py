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

def find_name(name1, name2):
    if levenshtein_distance(name1, name2) <= 1:
        return 1
    else:
        return -1

def findConfidenceLevel(first_name1, last_name1, rna_first_name1, rna_last_name1, first_name2, last_name2, rna_first_name2, rna_last_name2):
    if first_name1 == '' and last_name1 == '' or first_name2 == '' and last_name2 == '':
        return 0
    if first_name1 == '' or first_name2 == '':
        return find_name(last_name1, last_name2)
    else:
        return find_name(first_name1, first_name2)

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

def find_DOB(dob1, dob2):
    if dob1 == 'U' or dob2 == 'U':
        return 1
    elif levenshtein_distance(dob1, dob2) <= 1:
        return 0
    else:
        return -1

# more related to cleaning
def find_Gender(g1, g2):
    if g1 == 'U' or g2 == 'U':
        return 1
    elif g1 == g2:
        return 0
    else:
        return -1

def compare_address(address1, address2):
    if address1 == 'U' or address2 == 'U':
        return 1
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
    if min_street / levenshtein_sum < 1:
        return -1
    else:
        return 0

# clean cities
def find_city(city1, city2):
    if city1 == 'U' or city2 == 'U':
        return 1
    elif levenshtein_distance(city1, city2) <= 1:
        return 0
    else:
        return -1

# clean state
def find_state(state1, state2):
    if state1 == 'XX' or state2 == 'XX':
        return 1
    elif state1 == state2:
        return 0
    else:
        return -1

# clean zipcode
def find_zipcode(zip1, zip2):
    if zip1 == 'U' or zip2 == 'U':
        return 1
    elif levenshtein_distance(str(zip1), str(zip2)) <= 1:
        return 0
    else:
        return -1

def find_account_number(ac1, ac2):
    if ac1 == 'U' or ac2 == 'U':
        return 1
    elif ac1 == ac2:
        return 0
    else:
        return -1
    
def compare_patients(patient1, patient2):
    mismatches = 0
    checked = 0
    if find_account_number(patient1['Patient Acct #'], patient2['Patient Acct #']) == 0:
        return 100
    conf1 = findConfidenceLevel(patient1['First Name'], patient1['Last Name'], patient1['rnaFirstName'], patient1['rnaLastName'], patient2['First Name'], patient2['Last Name'], patient2['rnaFirstName'], patient2['rnaLastName'])
    if conf1 == 0:
        mismatches += 1
    elif conf1 == 1:
        checked += 1
    elif conf1 == -1:
        checked += 1
        mismatches += 1
    elif conf1 < 76:
        mimatches += 1
    dob = find_DOB(patient1['dob_string'], patient2['dob_string'])
    if dob == 1:
        checked += 1
    elif dob == -1:
        mismatches += 1
    gender = find_Gender(patient1['Sex'], patient2['Sex'])
    if gender == 1:
        checked += 1
    elif gender == -1:
        mismatches += 1
    address = compare_address(patient1['cleaned street'], patient2['cleaned street'])
    if address == 1:
        checked += 1
    elif address == -1:
        mismatches += 1
    city = find_city(patient1['Current City'], patient2['Current City'])
    if city == 1:
        checked += 1
    elif city == -1:
        mismatches += 1
    state = find_state(patient1['Current State'], patient2['Current State'])
    if state == 1:
        checked += 1
    elif state == -1:
        mismatches += 1
    zip = find_zipcode(patient1['Current Zip Code'], patient2['Current Zip Code'])
    if zip == 1:
        checked += 1
    elif zip == -1:
        mismatches += 1
    
    if mismatches > 1 or checked >= 4:
        return 0
    else:
        return 100
    
def generate_confidence_matrix(confidence_func, df, threshold):
    matrix = np.zeros((df.shape[0], df.shape[0]))
    for index1, row1 in df.iterrows():
        for index2, row2 in df.iterrows():
            conf = confidence_func(
                    row1,
                    row2
            )
            if conf > threshold:
                matrix[index1][index2] = 1
            else:
                matrix[index1][index2] = 0
    return matrix

def calculate_connected_components(adjacency_matrix):
    graph = csr_matrix(adjacency_matrix)
    return connected_components(csgraph=graph, directed=False, return_labels=True)