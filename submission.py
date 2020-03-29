from data_cleaning import *
from evaluation import *
from confidence_aggregation import *
from levenshtein_distance_stats import *
from clustering import *
import fuzzy
soundex = fuzzy.Soundex(4)
FILENAME = 'Patient Matching Data.csv'

df_patient = load_and_clean_data(FILENAME)

matrix = generate_confidence_matrix(findConfidenceLevel, df_patient, 80, df_patient.shape[0])
n_components, labels = calculate_connected_components(matrix)
tp, fp, tn, fn = calculate_unbiased_confusion(labels, df_patient)

print('Accuracy: {}, Precision: {}, Recall: {}, F1: {}'.format(
    calculate_accuracy(tp, fp, tn, fn),
    calculate_precision(tp, fp, tn, fn),
    calculate_accuracy(tp, fp, tn, fn),
    calculate_F1_score(tp, fp, tn, fn)
))

print('TP: {}, FP: {}, TN: {}, FN: {}'.format(tp, fp, tn, fn))