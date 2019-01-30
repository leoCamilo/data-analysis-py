import numpy as np
import pandas as pd

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

# print(correlation(subway_df['ENTRIESn_hourly'], subway_df['meanprecipi']))
# print(correlation(subway_df['ENTRIESn_hourly'], subway_df['ENTRIESn']))

# ==========================================================================