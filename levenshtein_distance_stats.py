from Levenshtein import distance as levenshtein_distance
from random import sample
import fuzzy
soundex = fuzzy.Soundex(4)

def generate_balanced_match_data(df):
    matching_rows = []
    not_matching_rows = []
    for index1, row1 in df.iterrows():
        for index2, row2 in df.iterrows():
            if row1['GroupID'] == row2['GroupID']:
                matching_rows.append((row1, row2))
            else:
                not_matching_rows.append((row1, row2))
    matching_rows.extend(sample(not_matching_rows, len(matching_rows)))
    return matching_rows

def generate_decision_confidence(df, func):
    rows = generate_balanced_match_data(df)
    num_correct = 0
    num_wrong = 0
    for row_pair in rows:
        row1, row2 = row_pair
        if func(row1, row2):
            if row1['GroupID'] == row2['GroupID']:
                num_correct += 1
            else:
                num_wrong += 1
    return num_correct / (num_wrong + num_correct)

def generate_decision_accuracy(df, func):
    rows = generate_balanced_match_data(df)
    num_correct = 0
    num_wrong = 0
    for row_pair in rows:
        row1, row2 = row_pair
        if row1['GroupID'] == row2['GroupID']:
            if func(row1, row2):
                num_correct += 1
            else:
                num_wrong += 1
        else:
            if func(row1, row2):
                num_wrong += 1
            else:
                num_correct += 1
    return num_correct / (num_wrong + num_correct)

def generate_Ldist_df(df, column):
    confidences = dict()
    i = 0
    for index1, row1 in df.iterrows():
        for index2, row2 in df.iterrows():
            isSame = 0
            if row1["GroupID"] == row2["GroupID"]:
                isSame = 1
            confidences[i] = {
                'index1': index1,
                'index2': index2,
                'Ldist': levenshtein_distance(
                    row1[column],
                    row2[column]
                ),
                'isSame':isSame
            }
            i += 1
    return pd.DataFrame.from_dict(confidences, orient='index')

def generate_levenshtein_stats(df):
    dob_conf_stats = generate_Ldist_df(df, "dob_string")
    first_name_conf_stats = generate_Ldist_df(df, "rnaFirstName")
    last_name_conf_stats = generate_Ldist_df(df, "rnaLastName")
    gender_conf_stats = generate_Ldist_df(df, "Sex")
    return dob_conf_stats, first_name_conf_stats, last_name_conf_stats, gender_conf_stats