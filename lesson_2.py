import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# def read_csv(filename): return list(csv.DictReader(open(filename, 'r')))

# daily_engagement = read_csv('./data/daily_engagement_full.csv')

# def get_unique_students(data):	# use map to improve
# 	unique_students = set()

# 	for d in data:
# 		unique_students.add(d['acct'])

# 	return unique_students

# unique_engagement_students = get_unique_students(daily_engagement)

# ==================================================================================

# daily_engagement = pd.read_csv('./data/daily_engagement_full.csv')
# print(len(daily_engagement['acct'].unique()))

# ==================================================================================

# values = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

# def standardize_data(values):
# 	'''
# 	Fill in this function to return a standardized version of the given values,
# 	which will be in a NumPy array. Each value should be translated into the
# 	number of standard deviations that value is away from the mean of the data.
# 	(A positive number indicates a value higher than the mean, and a negative
# 	number indicates a value lower than the mean.)
# 	'''

# 	# standardize_data = []

# 	# mean = np.mean(values)
# 	# std = np.std(values)

# 	# for data in values:
# 	#     standardize_data.append((data - mean)/std)

# 	# return np.array(standardize_data)

# 	return (values - values.mean()) / values.std()

# print(standardize_data(values))

# ==================================================================================

# def mean_time_for_paid_students(time_spent, days_to_cancel):
#     tsmt1w = time_spent[days_to_cancel >= 7]
#     return tsmt1w.mean()

# # Time spent in the classroom in the first week for 20 students
# time_spent = np.array([
#        12.89697233,    0.        ,   64.55043217,    0.        ,
#        24.2315615 ,   39.991625  ,    0.        ,    0.        ,
#       147.20683783,    0.        ,    0.        ,    0.        ,
#        45.18261617,  157.60454283,  133.2434615 ,   52.85000767,
#         0.        ,   54.9204785 ,   26.78142417,    0.
# ])

# # Days to cancel for 20 students
# days_to_cancel = np.array([
#       4,   5,  37,   3,  12,   4,  35,  38,   5,  37,   3,   3,  68,
#      38,  98,   2, 249,   2, 127,  35
# ])

# print(mean_time_for_paid_students(time_spent, days_to_cancel))

# ==================================================================================

gdp = pd.read_csv('./data/gdp_per_capita.csv', index_col='Country')
employment = pd.read_csv('./data/employment_above_15.csv', index_col='Country')
male_completion = pd.read_csv('./data/male_completion_rate.csv', index_col='Country')
life_expectancy = pd.read_csv('./data/life_expectancy.csv', index_col='Country')
female_completion = pd.read_csv('./data/female_completion_rate.csv', index_col='Country')

# The following code creates a Pandas Series for each variable for the United States.
# You can change the string 'United States' to a country of your choice.

employment_us = employment.loc['United States']
female_completion_us = female_completion.loc['United States']
male_completion_us = male_completion.loc['United States']
life_expectancy_us = life_expectancy.loc['United States']
gdp_us = gdp.loc['United States']

# plt.hist(gdp_us)
plt.plot(gdp_us)
plt.show()

# Use the Series defined above to create a plot of each variable over time for
# the country of your choice. You will only be able to display one plot at a time
# with each "Test Run".