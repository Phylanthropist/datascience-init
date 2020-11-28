# I want to have a set of functions to flag certain practices that are perhaps prescribing drugs
# What we need to do!
# We need prescription data and practice data
# We need a function that calculates the Z-score of the opioid prescription rate
# We need a Z-score cut-off
# We are going to implement as a command line script using the argsparse

# Steps:
# 1. Load and clean the data
# 2. We flag opioids
# 3. Perform the merges and data analysis
# 4. Sort and find those that are suspicious
import pandas as pd
import numpy as np


def load_and_clean_data():
    """Returns the cleaned scripts, practices and chemical data sets"""
    scripts = pd.read_csv('/home/michael/PycharmProjects/pythonProject/dw-data/201701scripts_sample.csv.gz')

    col_names = ['code', 'name', 'addr_1', 'addr_2', 'borough', 'village', 'post_code']
    practices = pd.read_csv('/home/michael/PycharmProjects/pythonProject/dw-data/practices.csv.gz', names=col_names)

    # Need to drop duplicates CHEM SUB rows
    chem = pd.read_csv('/home/michael/PycharmProjects/pythonProject/dw-data/chem.csv.gz')
    chem = chem.sort_values('CHEM SUB').drop_duplicates(subset='CHEM SUB', keep='first')
    return scripts, practices, chem


def flag_opioids(chem):
    """Add column to data frame flaging prescription if it is an opioids"""
    chem = chem.copy()
    # Takes a copy of the chem data set so as not to mutate the dataset
    opioids = ['morphine', 'oxycodone', 'methadone', 'fentanyl', 'pethidine', 'buprenorphine', 'propoxyphene',
               'codeine']
    chem['is_opioids'] = chem['NAME'].str.lower().str.contains(r'|'.join(opioids))
    return chem


def calculate_Z_score(scripts, chem):
    """Return a series of the Z-score for each practice"""
    scripts_with_chem = scripts.merge(chem[['CHEM SUB', 'is_opioids']],
                                      left_on='bnf_code', right_on='CHEM SUB',
                                      how='left').fillna(False)
    # Calculate the Z-score for each practice
    opioids_per_practice = scripts_with_chem.groupby('practice')['is_opioids'].mean()
    relative_opioids_per_practice = opioids_per_practice - scripts_with_chem['is_opioids'].mean()
    standard_error_per_practice = scripts_with_chem['is_opioids'].std() / np.sqrt(scripts_with_chem['practice'].
                                                                                  value_counts())
    opioids_score = relative_opioids_per_practice / standard_error_per_practice
    return opioids_score


def flag_anomalous_practices(practices, opioids_score, scripts, z_score_cutoff=2, raw_count_cutoff=50):
    """Return practices that have a z-score and count greater than cutoff"""
    unique_practices = practices.sort_values('name').drop_duplicates(subset='code', keep='first')
    unique_practices = unique_practices.set_index('code')
    unique_practices['z_score'] = opioids_score
    unique_practices['counts'] = scripts['practice'].value_counts()
    result = unique_practices.sort_values('z_score', ascending=False).head(100)
    return result.query('z_score > @z_score_cutoff and counts > @raw_count_cutoff')


def dump_data(results):
    """Dump pandas data frame of the results to disk"""
    results.to_csv('practices_flagged.csv', index=False)


if __name__ == '__main__':
    import sys

    print(f"Running {sys.argv[0]}")

    z_score_cutoff = int(sys.argv[1])
    raw_count_cutoff = int(sys.argv[2])  # Had to convert to integer before passing it as an argument in line 80 and 81

    scripts, practices, chem = load_and_clean_data()
    chem = flag_opioids(chem)
    opioids_score = calculate_Z_score(scripts, chem)
    anomalous_practices = flag_anomalous_practices(practices, opioids_score, scripts,
                                                   z_score_cutoff=z_score_cutoff,
                                                   raw_count_cutoff=raw_count_cutoff)
    dump_data(anomalous_practices)

# It would be a best practice to make our program more dynamic by providing instances where the cutoff and
# raw count value can be externally added when the program runs. If the values are not dynamically typed in
# then anytime we make changes git will have to show a difference
