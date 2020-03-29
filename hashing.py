import pandas as pd
import hashlib

def full_name_hash(first_name, last_name, gender, dob):
    SALT = 'OATEST'
    hasher = hashlib.sha1()
    hasher.update('{}{}~{}{}'.format(SALT, dob, gender, first_name).encode('utf-8'))
    return '{}~{}'.format(hasher.hexdigest(), last_name)

def partial_hash(first_name, last_name, gender, dob):
    # first three of first and last name
    first_name = first_name[:3] if len(first_name) >= 3 else 'X' * (3 - len(first_name)) + first_name
    last_name = last_name[:3] if len(last_name) >= 3 else 'X' * (3 - len(last_name)) + last_name 
    SALT = 'OATEST'
    hasher = hashlib.sha1()
    hasher.update('{}{}~{}{}'.format(SALT, dob, gender, first_name).encode('utf-8'))
    return '{}~{}'.format(hasher.hexdigest(), last_name)

def df_full_name_hash(x):
    return full_name_hash(x['First Name'], x['Last Name'], x['Sex'], x['dob_string'])

def df_partial_hash(x):
    return partial_hash(x['First Name'], x['Last Name'], x['Sex'], x['dob_string'])

def create_hash_tokens(df):
    df['full_name_hash'] = df.apply(df_full_name_hash, axis=1)
    df['partial_name_hash'] = df.apply(df_partial_hash, axis=1)

