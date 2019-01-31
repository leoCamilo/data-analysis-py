import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ridership = np.array([
    [   0,    0,    2,    5,    0],
    [1478, 3877, 3674, 2328, 2539],
    [1613, 4088, 3991, 6461, 2691],
    [1560, 3392, 3826, 4787, 2613],
    [1608, 4802, 3932, 4477, 2705],
    [1576, 3933, 3909, 4979, 2685],
    [  95,  229,  255,  496,  201],
    [   2,    0,    1,   27,    0],
    [1438, 3785, 3589, 4174, 2215],
    [1342, 4043, 4009, 4665, 3033]
])

def mean_riders_for_max_station(ridership):
    fst_day_station = ridership[0].argmax()
    overall_mean = ridership.mean()
    mean_for_max = ridership[:,fst_day_station].mean()
    
    return (overall_mean, mean_for_max)

def min_and_max_riders_per_day(ridership):
    daily_mean_per_station = ridership.mean(axis=0)
    max_daily_ridership = daily_mean_per_station.max()
    min_daily_ridership = daily_mean_per_station.min()
    
    return (max_daily_ridership, min_daily_ridership)

def correlation(x, y):                          # pearson's R | correlation coeficient
    std_x = (x - x.mean()) / x.std(ddof=0)
    std_y = (y - y.mean()) / y.std(ddof=0)

    return (std_x * std_y).mean()

subway_df = pd.read_csv('./data/nyc_subway_weather.csv')

# ============================ TEST CORRELATION ============================

# plt.plot(subway_df['ENTRIESn_hourly'], 'ro')
# plt.show()

# plt.plot(subway_df['ENTRIESn'], 'ro')
# plt.show()

# print(correlation(subway_df['ENTRIESn_hourly'], subway_df['meanprecipi']))
# print(correlation(subway_df['ENTRIESn_hourly'], subway_df['ENTRIESn']))

# ==========================================================================

def get_hourly_entries_and_exits(entries_and_exits):
    return entries_and_exits - entries_and_exits.shift(periods=1)
    # or
    # return entries_and_exits.diff()

grades_df = pd.DataFrame(
    data={'exam1': [43, 81, 78, 75, 89, 70, 91, 65, 98, 87], 'exam2': [24, 63, 56, 56, 67, 51, 79, 46, 72, 60]},
    index=['Andre', 'Barry', 'Chris', 'Dan', 'Emilio', 'Fred', 'Greta', 'Humbert', 'Ivan', 'James'])

def convert_grades(grades):
    def grade_parser(grade):
        if grade < 60: return 'F'
        elif grade < 70: return 'D'
        elif grade < 80: return 'C'
        elif grade < 90: return 'B'
        else: return 'A'

    return grades.applymap(grade_parser)

# ==================== TEST APPLYMAP ====================

# print(convert_grades(grades_df))

# =======================================================

def convert_grades_curve(exam_grades):
    # Pandas has a bult-in function that will perform this calculation
    # This will give the bottom 0% to 10% of students the grade 'F',
    # 10% to 20% the grade 'D', and so on. You can read more about
    # the qcut() function here:
    # http://pandas.pydata.org/pandas-docs/stable/generated/pandas.qcut.html
    
    return pd.qcut(exam_grades, [0, 0.1, 0.2, 0.5, 0.8, 1], labels=['F', 'D', 'C', 'B', 'A'])
        
# qcut() operates on a list, array, or Series. This is the
# result of running the function on a single column of the
# DataFrame.
# print(convert_grades_curve(grades_df['exam1']))

# qcut() does not work on DataFrames, but we can use apply()
# to call the function on each column separately
# print(grades_df.apply(convert_grades_curve))

def standardize(df):
    '''
    Fill in this function to standardize each column of the given
    DataFrame. To standardize a variable, convert each value to the
    number of standard deviations it is above or below the mean.
    '''

    return (df - df.mean()) / df.std(ddof=0)

def second_largest(df):
    def get_second_largest(column):
        first_largest = column.min()
        second_largest = first_largest
        
        for e in column:
            if first_largest < e:
                second_largest = first_largest
                first_largest = e
            elif e > second_largest:
                second_largest = e
        
        return second_largest
    
    return df.apply(get_second_largest)

def test_groupby():
    days_groups = subway_df.groupby('day_week')
    mean_by_day = days_groups['ENTRIESn_hourly'].mean()
    mean_by_day.plot(kind='line')
    plt.show()

# ======================================================= MERGE IS LIKE THE JOIN FROM SQL
# subway_df.merge(weather_df, on='DATEn', how='inner')
# subway_df.merge(weather_df, on=['DATEn', 'hour', 'latitude', 'longitude'], how='inner')
# subway_df.merge(weather_df, 
#   left_on=['DATEn', 'hour', 'latitude', 'longitude'],
#   right_on=['date', 'hour', 'latitude', 'longitude'],
#   how='inner')