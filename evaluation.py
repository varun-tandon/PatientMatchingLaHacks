import pandas as pd

def measure_accuracy(labels, df):
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    for index1, row1 in df.iterrows():
        for index2, row2 in df.iterrows():
            if index1 >= index2:
                continue
            if row1['GroupID'] == row2['GroupID']: # P
                if labels[index1] == labels[index2]: # T
                    tp += 1
                else:
                    fn += 1
            else: # N
                if labels[index1] == labels[index2]: # F
                    fp += 1
                else: # T
                    tn += 1
    return (tp, fp, tn, fn)