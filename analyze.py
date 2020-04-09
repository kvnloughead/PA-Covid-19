#!usr/bin/python
"""
Attempt to analyze PA covid-19 data.
"""

import numpy as np
import pandas as pd
from tabulate import tabulate


from parse_website import negative_tests, positive_tests, deaths

data = {'negatives': np.array(negative_tests), 
                'positives': np.array(positive_tests), 
                'deaths': np.array(deaths)}



total_tests = data['negatives'] + data['positives']
new_tests = [p1 - p2 for p1, p2 in zip(total_tests[:-1], total_tests[1:])]
new_tests.append(np.nan)
testing_growth_rate = [p1 / p2 for p1, p2 in zip(new_tests[:-1], total_tests[1:])]
testing_growth_rate.append(np.nan)
# print(testing_growth_rate)
# print(len(testing_growth_rate))


new_cases = [p1 - p2 for p1, p2 in zip(positive_tests[:-1], positive_tests[1:])]
new_cases.append(np.nan)

new_deaths = [p1 - p2 for p1, p2 in zip(deaths[:-1], deaths[1:])]
new_deaths.append(np.nan)

rate_of_positive = data['positives']/(data['negatives'] + data['positives'])

nominal_growth_rate = [p1 / p2 for p1, p2 in zip(new_cases[:-1], positive_tests[1:])]
nominal_growth_rate.append(np.nan)

# Using all weeks worth of data might skew the numbers since the testing growth rate was so
# much greater early on.   Thus I subseted testing_growth_rate when computing average_testing_growth_rate

average_testing_growth_rate = np.nanmean(testing_growth_rate[:10])
# not sure about accuracy of referring to this as "normalized"
normalized_testing = average_testing_growth_rate / testing_growth_rate
normalized_case_growth_rate = nominal_growth_rate * normalized_testing

# Not sure about terminology:
# nominal_growth_rate / testing_growth_rate = marginal_growth_rate?
marginal_growth_rate = np.array(nominal_growth_rate) / np.array(testing_growth_rate)

data['new_cases'] = new_cases
# data['new_deaths'] = new_deaths
data['rate_of_positive'] = rate_of_positive
data['nominal_growth_rate'] = nominal_growth_rate
data['testing_growth_rate'] = testing_growth_rate
# data['normalized_testing'] = normalized_testing
data['marginal_growth_rate'] = marginal_growth_rate
data['normalized_case_growth_rate'] = normalized_case_growth_rate

df = pd.DataFrame(data)

if __name__ == '__main__':
        print(tabulate(df, headers='keys', tablefmt='psql'))