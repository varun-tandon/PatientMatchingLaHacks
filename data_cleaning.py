import pandas as pd
from datetime import datetime, timedelta
from Levenshtein import distance as levenshtein_distance
import re

def swap_full_state_name(x):
    states = {
        "AK" : "Alaska",
        "AL" : "Alabama",
        "AR" : "Arkansas",
        "AS" : "American Samoa",
        "AZ" : "Arizona",
        "CA" : "California",
        "CO" : "Colorado",
        "CT" : "Connecticut",
        "DC" : "District of Columbia",
        "DE" : "Delaware",
        "FL" : "Florida",
        "GA" : "Georgia",
        "GU" : "Guam",
        "HI" : "Hawaii",
        "IA" : "Iowa",
        "ID" : "Idaho",
        "IL" : "Illinois",
        "IN" : "Indiana",
        "KS" : "Kansas",
        "KY" : "Kentucky",
        "LA" : "Louisiana",
        "MA" : "Massachusetts",
        "MD" : "Maryland",
        "ME" : "Maine",
        "MI" : "Michigan",
        "MN" : "Minnesota",
        "MO" : "Missouri",
        "MS" : "Mississippi",
        "MT" : "Montana",
        "NC" : "North Carolina",
        "ND" : "North Dakota",
        "NE" : "Nebraska",
        "NH" : "New Hampshire",
        "NJ" : "New Jersey",
        "NM" : "New Mexico",
        "NV" : "Nevada",
        "NY" : "New York",
        "OH" : "Ohio",
        "OK" : "Oklahoma",
        "OR" : "Oregon",
        "PA" : "Pennsylvania",
        "PR" : "Puerto Rico",
        "RI" : "Rhode Island",
        "SC" : "South Carolina",
        "SD" : "South Dakota",
        "TN" : "Tennessee",
        "TX" : "Texas",
        "UT" : "Utah",
        "VA" : "Virginia",
        "VI" : "Virgin Islands",
        "VT" : "Vermont",
        "WA" : "Washington",
        "WI" : "Wisconsin",
        "WV" : "West Virginia",
        "WY" : "Wyoming"
    }
    if len(x) < 3:
        return x.upper()
    else:
        min_lev_dist_state = 'XX'
        min_dist = 1000
        for abb, state in states.items():
            dist = levenshtein_distance(x, state)
            if dist < min_dist:
                min_lev_dist_state = abb
                min_dist = dist
        return min_lev_dist_state

def swap_abb_state_name(x):
    states = {
        "AK" : "Alaska",
        "AL" : "Alabama",
        "AR" : "Arkansas",
        "AS" : "American Samoa",
        "AZ" : "Arizona",
        "CA" : "California",
        "CO" : "Colorado",
        "CT" : "Connecticut",
        "DC" : "District of Columbia",
        "DE" : "Delaware",
        "FL" : "Florida",
        "GA" : "Georgia",
        "GU" : "Guam",
        "HI" : "Hawaii",
        "IA" : "Iowa",
        "ID" : "Idaho",
        "IL" : "Illinois",
        "IN" : "Indiana",
        "KS" : "Kansas",
        "KY" : "Kentucky",
        "LA" : "Louisiana",
        "MA" : "Massachusetts",
        "MD" : "Maryland",
        "ME" : "Maine",
        "MI" : "Michigan",
        "MN" : "Minnesota",
        "MO" : "Missouri",
        "MS" : "Mississippi",
        "MT" : "Montana",
        "NC" : "North Carolina",
        "ND" : "North Dakota",
        "NE" : "Nebraska",
        "NH" : "New Hampshire",
        "NJ" : "New Jersey",
        "NM" : "New Mexico",
        "NV" : "Nevada",
        "NY" : "New York",
        "OH" : "Ohio",
        "OK" : "Oklahoma",
        "OR" : "Oregon",
        "PA" : "Pennsylvania",
        "PR" : "Puerto Rico",
        "RI" : "Rhode Island",
        "SC" : "South Carolina",
        "SD" : "South Dakota",
        "TN" : "Tennessee",
        "TX" : "Texas",
        "UT" : "Utah",
        "VA" : "Virginia",
        "VI" : "Virgin Islands",
        "VT" : "Vermont",
        "WA" : "Washington",
        "WI" : "Wisconsin",
        "WV" : "West Virginia",
        "WY" : "Wyoming",
        'XX' : ''
    }
    min_lev_dist_state = 'XX'
    min_dist = 1000
    for abb in states.keys():
        dist = levenshtein_distance(x, abb)
        if dist < min_dist:
            min_lev_dist_state = abb
            min_dist = dist
    return min_lev_dist_state
    
def clean_state_data(df):
    df['Current State'].fillna('XX', inplace=True)
    df['Current State'] = df['Current State'].apply(swap_full_state_name)
    df['Current State'] = df['Current State'].apply(swap_abb_state_name)

def clean_zip_code(df):
    df['Current Zip Code'].fillna(0, inplace=True)
    df['Zip Code String'] = df['Current Zip Code'].apply(lambda x: str(x))
    df['Zip Code String'] = df['Zip Code String'].apply(lambda x: x[:5] if len(x) > 5 else x)
    df['Zip Code String'] = df['Zip Code String'].replace('0', '00000')
    df['Zip Code String'] = df['Zip Code String'].apply(lambda x: '00000' if not x.isdigit() else x)
    df['Zip Code String'] = df['Zip Code String'].apply(lambda x: x if len(x) >= 5 else (x + '0' * (5 - len(x))))
    df['National Area'] = df['Zip Code String'].apply(lambda x: int(x[0]))
    df['Sectional Center'] = df['Zip Code String'].apply(lambda x: int(x[1:3]))
    df['Delivery Area'] = df['Zip Code String'].apply(lambda x: int(x[3:]))

def convert_date_string(x):
    try:
        parsed_date = datetime.strptime(x['Date of Birth'], '%m/%d/%Y')
        x['dob_string'] = str(parsed_date.strftime('%Y%m%d'))
        return x
    except:
        try:
            bad_row = x['Date of Birth']
            bad_row_splits = bad_row.split('/')
            x['dob_string'] = bad_row_splits[2] + bad_row_splits[1] + bad_row_splits[0]
            return x
        except:
            return x

def clean_date_data(df):
    return df.apply(convert_date_string, axis=1)

def clean_sex_data(df):
    df['Sex'].fillna('U', inplace=True)
    df['Sex'] = df['Sex'].apply(lambda x: x[0].upper() if x[0].upper() in {'M', 'F'} else 'U')

def fill_empty_name_data(df):
    df['First Name'].fillna('', inplace=True)
    df['Last Name'].fillna('', inplace=True)

def normalize_patient_first_and_last_names(df):
    df['rnaFirstName'] = df['First Name'].apply(lambda x: re.sub(r'\W+', '', x))
    df['rnaLastName'] = df['Last Name'].apply(lambda x: re.sub(r'\W+', '', x))
    df['rnaFirstName'] = df['rnaFirstName'].apply(lambda x: ''.join([i if ord(i) < 128 else ' ' for i in x]))
    df['rnaLastName'] = df['rnaLastName'].apply(lambda x: ''.join([i if ord(i) < 128 else ' ' for i in x]))

def encode_name_columns(df):
    df['First Name'].fillna('', inplace=True)
    df['Last Name'].fillna('', inplace=True)
    df['First Name'] = df['First Name'].apply(lambda x: ''.join([i if ord(i) < 128 else ' ' for i in x]))
    df['Last Name'] = df['Last Name'].apply(lambda x: ''.join([i if ord(i) < 128 else ' ' for i in x]))
    
def clean_address_data(df):
    df['cleaned street'] = df['Current Street 1'].str.replace('[^0-9a-zA-Z ]', '').str.lower()
    df['cleaned street'] = df['cleaned street'].str.split(' ')
    df['cleaned street'].fillna('U', inplace = True)

def load_and_clean_data(filename):
    df_patient = pd.read_csv(filename)
    encode_name_columns(df_patient)
    clean_state_data(df_patient)
    clean_zip_code(df_patient)
    df_patient = clean_date_data(df_patient)
    clean_sex_data(df_patient)
    fill_empty_name_data(df_patient)
    normalize_patient_first_and_last_names(df_patient)
    clean_address_data(df_patient)
    return df_patient