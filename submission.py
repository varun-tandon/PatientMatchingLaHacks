from data_cleaning import *
from evaluation import *
from confidence_aggregation import *

FILENAME = 'Patient MAtching Data.csv'

df_patient = load_and_clean_data(FILENAME)
matrix = generate_confidence_matrix(find_Levenshtein_Conf_Name, df_patient, 80)
n_components, labels = calculate_connected_components(matrix)
tp, fp, tn, fn = calculate_confusion_matrix(labels, df_patient)

print('Accuracy: {}, Precision: {}, Recall: {}, F1: {}'.format(
    calculate_accuracy(tp, fp, tn, fn),
    calculate_precision(tp, fp, tn, fn),
    calculate_accuracy(tp, fp, tn, fn),
    calculate_F1_score(tp, fp, tn, fn)
))

print('TP: {}, FP: {}, TN: {}, FN: {}'.format(tp, fp, tn, fn))