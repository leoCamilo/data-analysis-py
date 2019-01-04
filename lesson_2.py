import csv
import pandas as pd

# def read_csv(filename): return list(csv.DictReader(open(filename, 'r')))

# daily_engagement = read_csv('./data/daily_engagement_full.csv')

# def get_unique_students(data):	# use map to improve
# 	unique_students = set()

# 	for d in data:
# 		unique_students.add(d['acct'])

# 	return unique_students

# unique_engagement_students = get_unique_students(daily_engagement)

daily_engagement = pd.read_csv('./data/daily_engagement_full.csv')
print(len(daily_engagement['acct'].unique()))