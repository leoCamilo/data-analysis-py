import csv
import numpy as np
from datetime import datetime as dt
from collections import defaultdict
from functools import reduce

submissions_filename	= './data/project_submissions.csv'
engagement_filename		= './data/daily_engagement.csv'
enrollments_filename	= './data/enrollments.csv'

def get_csv(filename): return list(csv.DictReader(open(filename, 'r')))
def parse_date(date): return None if date == '' else dt.strptime(date, '%Y-%m-%d')
def parse_maybe_int(i): return None if i == '' else int(i)

enrollments = get_csv(enrollments_filename)
daily_engagement = get_csv(engagement_filename)
project_submissions = get_csv(submissions_filename)

udacity_test_accounts = set()
enrollment_users_set = set()
engagement_users_set = set()
submission_users_set = set()

for e in enrollments:
	e['days_to_cancel']	= parse_maybe_int(e['days_to_cancel'])
	e['account_key']	= parse_maybe_int(e['account_key'])
	e['cancel_date']	= parse_date(e['cancel_date'])
	e['join_date']		= parse_date(e['join_date'])
	e['is_udacity']		= e['is_udacity'] == 'True'
	e['is_canceled']	= e['is_canceled'] == 'True'

	enrollment_users_set.add(e['account_key'])

	if e['is_udacity']:
		udacity_test_accounts.add(e['account_key'])

for engagement in daily_engagement:
	engagement['account_key'] = parse_maybe_int(engagement['acct'])
	engagement['lessons_completed']	= float(engagement['lessons_completed'])
	engagement['total_minutes_visited']	= float(engagement['total_minutes_visited'])
	engagement['utc_date'] = parse_date(engagement['utc_date'])
	engagement_users_set.add(engagement['account_key'])

	del engagement['acct']

for submission in project_submissions:
	submission['account_key'] = parse_maybe_int(submission['account_key'])
	submission_users_set.add(submission['account_key'])

print('\n')

print(' enrollment_num_rows: {0}'.format(len(enrollments)))
print(' engagement_num_rows: {0}'.format(len(daily_engagement)))
print(' submission_num_rows: {0}'.format(len(project_submissions)))

print('\n\n============================\n\n')

print(' enrollment_num_unique_students: {0}'.format(len(enrollment_users_set)))
print(' engagement_num_unique_students: {0}'.format(len(engagement_users_set)))
print(' submission_num_unique_students: {0}'.format(len(submission_users_set)))

print('\n\n============================\n\n')

def remove_udacity_accounts(data):
	non_udacity_data = []
		
	for data_point in data:
		if data_point['account_key'] not in udacity_test_accounts:
			non_udacity_data.append(data_point)
		
	return non_udacity_data

non_udacity_enrollments = remove_udacity_accounts(enrollments)
non_udacity_engagement = remove_udacity_accounts(daily_engagement)
non_udacity_submissions = remove_udacity_accounts(project_submissions)

print(' non_udacity_engagement: {0}'.format(len(non_udacity_engagement)))
print(' non_udacity_enrollments: {0}'.format(len(non_udacity_enrollments)))
print(' non_udacity_submissions: {0}'.format(len(non_udacity_submissions)))

print('\n\n============================\n\n')

not_engaged_users = 0

for e in enrollments:
	if ((e["account_key"] not in engagement_users_set) and (e['cancel_date'] != e['join_date'])):
		not_engaged_users += 1

paid_students = {}

for e in non_udacity_enrollments:
	acck = e['account_key']
	jd = e['join_date']

	if (e['days_to_cancel'] == None or e['days_to_cancel'] > 7) and (acck not in paid_students or jd > paid_students[acck]):
		paid_students[acck] = jd

print(' paid_students: {0}'.format(len(paid_students)))
print('\n\n============================\n\n')

def remove_free_trial_cancels(data):
	new_data = []

	for data_point in data:
		if (data_point['account_key'] in paid_students):
			new_data.append(data_point)
		
	return new_data

paid_enrollments = remove_free_trial_cancels(non_udacity_enrollments)
paid_engagements = remove_free_trial_cancels(non_udacity_engagement)
paid_submissions = remove_free_trial_cancels(non_udacity_submissions)

print(' paid_enrollments: {0}'.format(len(paid_enrollments)))
print(' paid_engagements: {0}'.format(len(paid_engagements)))
print(' paid_submissions: {0}'.format(len(paid_submissions)))

print('\n\n============================\n\n')

paid_engagement_in_first_week = []

def within_one_week(join_date, engagement_date):
	days_past = (engagement_date - join_date).days
	return 0 <= days_past < 7

for e in paid_engagements:
	if within_one_week(paid_students[e['account_key']], e['utc_date']):
		paid_engagement_in_first_week.append(e)

print(' paid_engagement_in_first_week: {0}'.format(len(paid_engagement_in_first_week)))
print('\n\n============================\n\n')

def get_total_columm_value(columm, data):
	total_data_by_account = {}
	
	for acck, data_list in data.items():
		just_engagement_values = list(map((lambda e: e[columm]), data_list))
		total_data_by_account[acck] = reduce((lambda agg, data_col: agg + data_col), just_engagement_values)

	return total_data_by_account

engagement_by_account = defaultdict(list)

for e in paid_engagement_in_first_week:
	engagement_by_account[e['account_key']].append(e)

total_minutes_by_account = get_total_columm_value('total_minutes_visited', engagement_by_account)
total_lessons_by_account = get_total_columm_value('lessons_completed', engagement_by_account)

total_minutes_by_account_list = list(total_minutes_by_account.values())
total_lessons_by_account_list = list(total_lessons_by_account.values())

print(' total_minutes [mean]: {0}'.format(np.mean(total_minutes_by_account_list)))
print(' total_minutes [standart deviation]: {0}'.format(np.std(total_minutes_by_account_list)))
print(' total_minutes [minimum]: {0}'.format(np.min(total_minutes_by_account_list)))
print(' total_minutes [maximum]: {0}'.format(np.max(total_minutes_by_account_list)))

print('\n\n============================\n\n')

print(' total_lessons [mean]: {0}'.format(np.mean(total_lessons_by_account_list)))
print(' total_lessons [standart deviation]: {0}'.format(np.std(total_lessons_by_account_list)))
print(' total_lessons [minimum]: {0}'.format(np.min(total_lessons_by_account_list)))
print(' total_lessons [maximum]: {0}'.format(np.max(total_lessons_by_account_list)))

print('\n\n============================\n\n')