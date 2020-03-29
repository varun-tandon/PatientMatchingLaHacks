from data_cleaning import *
from evaluation import *
from confidence_aggregation import *
from levenshtein_distance_stats import *
from clustering import *
from voting import *
from hashing import *
import fuzzy
soundex = fuzzy.Soundex(4)

FILENAME = 'Patient Matching Data.csv'

df_patient = load_and_clean_data(FILENAME)

create_hash_tokens(df_patient)

matrix = generate_ensemble_votes(df_patient)
n_components, labels = calculate_connected_components(matrix)
df_patient['grouping'] = pd.Series(labels)
df_patient.to_csv('result.csv')

# Accuracy Statistics (removed for submission purposes)
# tp, fp, tn, fn = calculate_confusion_matrix(labels, df_patient)

# print('Accuracy: {}, Precision: {}, Recall: {}, F1: {}'.format(
#     calculate_accuracy(tp, fp, tn, fn),
#     calculate_precision(tp, fp, tn, fn),
#     calculate_accuracy(tp, fp, tn, fn),
#     calculate_F1_score(tp, fp, tn, fn)
# ))

# print('TP: {}, FP: {}, TN: {}, FN: {}'.format(tp, fp, tn, fn))
