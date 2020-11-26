import pandas as pd
import numpy as np
import gzip
import matplotlib

# load the 2017 data
with gzip.open('/home/michael/PycharmProjects/pythonProject/dw-data/201701scripts_sample.csv.gz', 'rb') as f:
    scripts = pd.read_csv(f)
# scripts.head()
# print(scripts)

col_names = ['code', 'name', 'addr_1', 'addr_2', 'borough', 'village', 'post_code']
with gzip.open('/home/michael/PycharmProjects/pythonProject/dw-data/practices.csv.gz', 'rb') as f_prac:
    practices = pd.read_csv(f_prac, names=col_names, header=None)
practices.head()

with gzip.open('/home/michael/PycharmProjects/pythonProject/dw-data/chem.csv.gz', 'rb') as f_chem:
    chem = pd.read_csv(f_chem)
chem.head()

with gzip.open('/home/michael/PycharmProjects/pythonProject/dw-data/201606scripts_sample.csv.gz', 'rb') as f_practice_2:
    scripts16 = pd.read_csv(f_practice_2)


# print(scripts16.head())


# Question 1: summary_statistics
def summary(key):
    total = scripts[key].sum()
    avg = scripts[key].describe()[1]
    s = scripts[key].describe()[2]
    q25 = scripts[key].describe()[4]
    med = scripts[key].describe()[5]
    q75 = scripts[key].describe()[6]
    return total, avg, s, q25, med, q75


summary_stats = [('items', summary('items')),
                 ('quantity', summary('quantity')),
                 ('nic', summary('nic')),
                 ('act_cost', summary('act_cost'))]

# Question 2: most_common_item

item_by_bnf_name = scripts.groupby(['bnf_name'], sort=False)['items'].sum()
item_by_bnf_name2 = pd.DataFrame({'bnf_name': item_by_bnf_name.index, 'items': item_by_bnf_name.values})
max_index_position = item_by_bnf_name2['items'].idxmax()
# Use the index of the maximum position to get the values for bnf_name and items
answer = item_by_bnf_name2.loc[max_index_position]
answer_holder = (answer['bnf_name'], answer['items'])
most_common_item = [answer_holder]
# print(most_common_item)

# Question 3 : Items by Region
practices_unique = practices.sort_values('post_code').drop_duplicates(subset='code', keep='first')
scripts_with_practices = scripts.merge(practices_unique, left_on='practice', right_on='code', how='left')
output = scripts_with_practices.groupby(['post_code', 'bnf_name'])['items'].sum().reset_index().set_index('post_code')
# Total items across each postal code
total = output.groupby('post_code')['items'].sum()
output['total'] = total
output['ratio'] = output['items'] / output['total']
# Most times apply method can be the best strategy to devise in performing a said operation over a group.
result = output.groupby('post_code').apply(lambda df: df.sort_values('ratio', ascending=False).iloc[0])
# Alternative method using nlargest()
result2 = output.groupby('post_code').apply(lambda df: df.nlargest(1, 'ratio'))
items_by_region = result.reset_index()[['post_code', 'bnf_name', 'ratio']]
# print(items_by_region.head(100))

# Question 4 : Scripts anomalies
opioids = ['morphine', 'oxycodone', 'methadone', 'fentanyl', 'pethidine', 'buprenorphine', 'propoxyphene', 'codeine']
chem = chem.sort_values('CHEM SUB').drop_duplicates(subset='CHEM SUB', keep='first')
chem['is_opioids'] = chem['NAME'].str.lower().str.contains(r'|'.join(opioids))
print(chem)
scripts2017_with_chem = scripts.merge(chem[['CHEM SUB', 'is_opioids']],
                                      left_on='bnf_code', right_on='CHEM SUB',
                                      how='left').fillna(False)
opioids_per_practice = scripts2017_with_chem.groupby('practice')['is_opioids'].mean()
true_mean_is_opioids_allprac = scripts2017_with_chem['is_opioids'].mean()
relative_opioids_per_practice = opioids_per_practice - true_mean_is_opioids_allprac
total_std_is_opioids = scripts2017_with_chem['is_opioids'].std()
counts_per_practice = scripts2017_with_chem['practice'].value_counts()
standard_error_per_practice = total_std_is_opioids / np.sqrt(counts_per_practice)
opioids_score = relative_opioids_per_practice / standard_error_per_practice
unique_practices = practices.sort_values('name').drop_duplicates(subset='code', keep='first')
unique_practices = unique_practices.set_index('code')
unique_practices['z_score'] = opioids_score
unique_practices['counts'] = scripts2017_with_chem['practice'].value_counts()
unique_practices = unique_practices.sort_values('z_score', ascending=False).head(100)
result = unique_practices[['name', 'z_score', 'counts']]
# print(result)

# Question 5: script_growth
percentage_growth = ((scripts['bnf_name'].value_counts() - scripts16['bnf_name'].value_counts()) / scripts['bnf_name'].
                     value_counts())
percentage_growth.name = 'growth_rate'
result1 = (percentage_growth.to_frame().assign(raw_count=scripts16['bnf_name'].value_counts())
           .query('raw_count>50')
           .dropna()
           .reset_index()
           .sort_values('growth_rate', ascending=False)
           .rename(columns={'index': 'script_name'}))  # rename({'index':'script_name'}, axis=1)
# print(result1)

# Question 6: Rare Scripts
p = 1 / scripts['bnf_code'].nunique()
rate = scripts['bnf_code'].value_counts() / len(scripts)
rare_codes = rate < 0.1 * p
scripts = scripts.set_index('bnf_code')
scripts['rare'] = rare_codes
rare_cost_total = scripts.query('rare==True').groupby('practice')['act_cost'].sum()
all_cost_total = scripts.groupby('practice')['act_cost'].sum()
rare_cost_prop = (rare_cost_total / all_cost_total).fillna(0)
# Note anytime we do a mathematical operation on a series there tend to be missing values.
relative_rare_cost_prop = rare_cost_prop - scripts.query('rare == True')['act_cost'].sum() / scripts['act_cost'].sum()
standard_error = relative_rare_cost_prop.std()
rare_scores = relative_rare_cost_prop / standard_error
unique_practices['rare_score'] = rare_scores
final_answer = (unique_practices.sort_values('rare_score', ascending=False)).reset_index().loc[:, ['code', 'name',
                                                                                                   'rare_score']].head(
    100)
# print(final_answer)
# print(rare_scores.loc['Y03472'])
