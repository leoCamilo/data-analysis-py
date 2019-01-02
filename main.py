import csv
import numpy as np
import matplotlib.pyplot as plt
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
	engagement['num_courses_visited'] = float(engagement['num_courses_visited'])
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

def group_data_by_acc(columm, data):
	data_by_account = defaultdict(list)

	for d in data:
		data_by_account[d[columm]].append(d)

	return data_by_account

def get_total_columm_value(columm, data):
	total_data_by_account = {}
	
	for acck, data_list in data.items():
		just_engagement_values = list(map((lambda e: e[columm]), data_list))
		total_data_by_account[acck] = reduce((lambda agg, data_col: agg + data_col), just_engagement_values)

	return total_data_by_account

def show_metrics(description, data_list):
	print(' {0} [mean]: {1}'.format(description, np.mean(data_list)))
	print(' {0} [minimum]: {1}'.format(description, np.min(data_list)))
	print(' {0} [maximum]: {1}'.format(description, np.max(data_list)))
	print(' {0} [standart deviation]: {1}'.format(description, np.std(data_list)))

engagement_by_account = group_data_by_acc('account_key', paid_engagement_in_first_week)

total_minutes_by_account = get_total_columm_value('total_minutes_visited', engagement_by_account)
total_lessons_by_account = get_total_columm_value('lessons_completed', engagement_by_account)

total_minutes_by_account_list = list(total_minutes_by_account.values())
total_lessons_by_account_list = list(total_lessons_by_account.values())

show_metrics('total_minutes', total_minutes_by_account_list)

print('\n\n============================\n\n')

show_metrics('total_lessons', total_lessons_by_account_list)

print('\n\n============================\n\n')

def get_total_unique_columm_value(columm, data):
	total_data_by_account = {}
	
	for acck, data_list in data.items():
		just_engagement_values = list(map((lambda e: 1 if e[columm] > 0 else 0), data_list))
		total_data_by_account[acck] = reduce((lambda agg, data_col: agg + data_col), just_engagement_values)

	return total_data_by_account

num_courses_visited = get_total_unique_columm_value('num_courses_visited', engagement_by_account)
total_num_courses_visited = list(num_courses_visited.values())

show_metrics('num_courses_visited', total_num_courses_visited)

print('\n\n============================\n\n')

subway_project_lesson_keys = ['746169184', '3176718735']
project_passing_keys = ['PASSED', 'DISTINCTION']
pass_subway_project_by_user = set()
non_passing_engagement = []
passing_engagement = []

for submission in paid_submissions:
	if (submission['lesson_key'] in subway_project_lesson_keys) and (submission['assigned_rating'] in project_passing_keys):
		pass_subway_project_by_user.add(submission['account_key'])

for engagement in paid_engagement_in_first_week:
	if engagement['account_key'] in pass_subway_project_by_user:
		passing_engagement.append(engagement)
	else:
		non_passing_engagement.append(engagement)

print(' passing_engagement: {0}'.format(len(passing_engagement)))
print(' non_passing_engagement: {0}'.format(len(non_passing_engagement)))

print('\n\n============================\n\n')

passing_engagement_by_account = group_data_by_acc('account_key', passing_engagement)
non_passing_engagement_by_account = group_data_by_acc('account_key', non_passing_engagement)

total_minutes_by_account_pass = get_total_columm_value('total_minutes_visited', passing_engagement_by_account)
lessons_completed_by_account_pass = get_total_columm_value('lessons_completed', passing_engagement_by_account)
total_minutes_by_account_non_pass = get_total_columm_value('total_minutes_visited', non_passing_engagement_by_account)
lessons_completed_by_account_non_pass = get_total_columm_value('lessons_completed', non_passing_engagement_by_account)

total_minutes_by_account_pass_list = list(total_minutes_by_account_pass.values())
total_minutes_by_account_non_pass_list = list(total_minutes_by_account_non_pass.values())
lessons_completed_by_account_pass_list = list(lessons_completed_by_account_pass.values())
lessons_completed_by_account_non_pass_list = list(lessons_completed_by_account_non_pass.values())

show_metrics('total_minutes passing studants', total_minutes_by_account_pass_list)
show_metrics('total_minutes non passing studants', total_minutes_by_account_non_pass_list)
show_metrics('lessons_completed passing studants', lessons_completed_by_account_pass_list)
show_metrics('lessons_completed non passing studants', lessons_completed_by_account_non_pass_list)

print('\n\n============================\n\n')

plt.hist(lessons_completed_by_account_non_pass_list)
plt.show()