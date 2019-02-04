import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

subway_df = pd.read_csv('./data/nyc_subway_weather.csv')


fig1, ax1 = plt.subplots()

subway_df.describe()

ax1.set_title('Basic BoxPlot')
ax1.boxplot(subway_df['ENTRIESn_hourly'])
plt.show()