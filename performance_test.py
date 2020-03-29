from data_cleaning import *
from evaluation import *
from confidence_aggregation import *
from levenshtein_distance_stats import *
from clustering import *
import fuzzy
soundex = fuzzy.Soundex(4)

def serial_date_to_string(srl_no):
    new_date = datetime(1970,1,1,0,0) + timedelta(srl_no - 1)
    return new_date.strftime("%Y%m%d")

def convert_external_data(filename):
    df = pd.read_csv(filename)
    df = df.rename(columns={
        'LAST': 'Last Name',
        'FIRST': 'First Name',
        'DOB': 'Date of Birth',
        'GENDER': 'Sex',
        'STATE': 'Current State',
        'ZIP': 'Current Zip Code',
        'ADDRESS1': 'Current Street 1'
    })
    df = df.dropna(subset=['Date of Birth'])
    df['dob_string'] = df['Date of Birth'].apply(lambda x: serial_date_to_string(x))
    df.to_csv('A-C_cleaned.csv')

FILENAME = 'A-C.csv'

df_patient = pd.read_csv('A-C_cleaned.csv')
print('Converting external data...')
convert_external_data(FILENAME)
print('Loading and cleaning data...')
df_patient = load_and_clean_data('A-C_cleaned.csv')
df_patient.to_csv('cleaned_performance_test.csv')
print('Generating confidence matrix...')
matrix = generate_confidence_matrix(findConfidenceLevel, df_patient, 80, 10)
n_components, labels = calculate_connected_components(matrix)
tp, fp, tn, fn = calculate_unbiased_confusion(labels, df_patient)

print('Accuracy: {}, Precision: {}, Recall: {}, F1: {}'.format(
    calculate_accuracy(tp, fp, tn, fn),
    calculate_precision(tp, fp, tn, fn),
    calculate_accuracy(tp, fp, tn, fn),
    calculate_F1_score(tp, fp, tn, fn)
))

print('TP: {}, FP: {}, TN: {}, FN: {}'.format(tp, fp, tn, fn))