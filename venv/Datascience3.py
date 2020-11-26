import gzip
import json
import statistics
import math


def caller():
    with gzip.open('/home/michael/PycharmProjects/pythonProject/pw-data/201701scripts_sample.json.gz', 'rb') as f:
        scripts = json.load(f)
    return scripts


# print(scripts[:])

with gzip.open('/home/michael/PycharmProjects/pythonProject/pw-data/practices.json.gz', 'rb') as f:
    practices = json.load(f)


# print(practices[:5])

# Question 1: SUMMARY STATISTICS

def describe(key):
    value_holder = []
    checker = caller()
    for val in checker:
        for k, v in val.items():
            if k == key:
                value_holder.append(v)
    # Sum of the values in items
    summ = sum(value_holder)
    # Mean of the values in items
    mean = statistics.mean(value_holder)
    # Standard deviation of the values in the items
    stdevh = statistics.pstdev(value_holder)
    # Median of the values in items
    median = statistics.median(value_holder)
    # First Quartile of the values in items
    y = sorted(value_holder)
    x = (len(y) + 1) // 4
    first_quart = y[x]
    # Third Quartile of the values in items
    x2 = (3 * (len(y) + 1)) // 4
    third_quart = y[x2]
    return summ, mean, stdevh, first_quart, median, third_quart


summary = [('items', describe('items')),
           ('quantity', describe('quantity')),
           ('nic', describe('nic')),
           ('act_cost', describe('act_cost'))]


# print(summary)


