from Levenshtein import distance as levenshtein_distance

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