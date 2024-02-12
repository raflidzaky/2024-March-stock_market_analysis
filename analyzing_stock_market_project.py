# -*- coding: utf-8 -*-
"""Data Analysis Project: Analyzing Stock Market.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15hujoJHjhT_T93XSk5qri5erxF6oAxpJ

# Environment Settings
This step includes installing packages of the stock market data set and import libraries. While the data set is ready, the next step is even more crucial: understanding the data.
"""

!pip install yfinance

# Data set package
import yfinance as yf

# Libraries for data wrangling and analyses
import datetime as dt
import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis
from statsmodels.tsa.stattools import adfuller

# Libraries for visualization: setting the charts ready
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.dates as mdt
import seaborn as sns

# Import the data set
dataset = yf.download('BAC', start='2004-01-01', end='2016-01-01')

# Read the data set
dataset

"""# Understanding Data set
Several tasks are need to be done:

1. **Understanding the table structure**
2. **Looking for data tidiness issue**
3. **Understanding structure of the data (dimension/columns).** This includes dimension definition

## **Understanding the table structure**
> Relevant questions:
- How much observations and columns exist in the data?
- What is the index of the table? Does current index relevant? If no/yes, why? (This question is vital prior to data visualization practice).
- How do the data type? Do they consistent?
"""

dataset.info()

"""Apparently, there are 7 columns in the data set. First one is index column (date-based format), the rest are information of the stock market. **Apparently, all of the price-related columns have a float data type, while volume is stored as integer**. The data set has **3021 records/observations** for every date index. We assume the index is unique unless stated otherwise in the next section.

Now, we could address the index format issue. Is it relevant? In this context, it will not relevant. As it will made the coordinate format, for any data visualization below, harder. This is true because the date could not directly processed by "calling" it like this

> ```dataset.index```

The next step is making the data set index as it should be, started with 0 until n numbers.



"""

# Make a column to store the date
dataset['Date'] = dataset.index

# Reorder the newest column to the first order
dataset = dataset.iloc[:, [6, 0, 1, 2, 3, 4, 5]]

# Changing the index incrementally
dataset.index = range(len(dataset['Open']))
dataset

"""## **Looking for data tidiness issue**
> Relevant questions:
> - Is it any missing value in the data?
> - Are there any rows that have duplicated values?

"""

dataset.isnull().sum()

# Check duplicated values in each rows
for column in dataset.columns:
  duplicate_state = dataset.duplicated(keep='first').sum()
  print(f'{column}', ' ', duplicate_state)

"""## **Understanding the structure of each dimension/columns**

> Relevant question:
> - What is the definition of each dimension? Knowing this would be useful to do analysis

The (simplified) definition of each dimension is following:
1. Open: Price of the first transaction in the a business day
2. High: Highest price for a traded security given the period, in this case is business day.
3. Low: Lowest price for a traded security given the period, in this case is business day.
4. Close: Price of the last transaction in the end of a business day
5. Adj. Close: This is a closing price w take account companies' action that affect the companies' stock values. Hence, this column reflect the underlying stock performance.
6. Volume: Total numbers of share traded at given day

# Exploratory Data Analysis

This exploratory data analysis will find out overall characteristics of our data. The difference between soon descriptive diagnostic is no narrative included, at least for this project.

My approach to do exploratory data analysis is a top down analysis. Coming from generic description (descriptive statistics and distribution analysis) and correlation heatmap.

Outlier analysis is not included in this project. Why? Since I use time-series data analysis, which cautiously non-stationary issues (such as trends, shocks, or else), that might have bunch significantly higher or lower data points (relative from the group).

## Generic Analysis
"""

dataset.describe()

def skewness_value(input):
  '''
      Logic of this function is to calculate skewness of each column within the data set.
      On top of that, scipy stats require an axis specification, otherwise, it'll ravel (flatten)
        the dataset and compute the skewness statistic as once.

      Thus, I specify the data set column and then I will no longer need to set axis specification in skew function.
      The next step is setting the for loop that compute the skew statistic. That for loop will also show which column is computed.
      For each operation done, the skewness variable will be updated according to next entry of input
  '''

  for i in input:
    skewness = dataset[i].skew(axis=None).round(3)
    print(i, ':', skewness)

# Input: Data set column specification
skewness_value(input=dataset.iloc[:, 1:7])

def kurtosis_value(input):
  '''
      This function triggers to check kurtosis value of each columns.
      Hence, I do a for loop to count each column's kurtosis without any hard-code.
      It is shown that the for loop address i-th column, which defined as the input (first until seventh columns)
  '''
  for i in input:
    kurtosis = dataset[i].kurtosis(axis=None).round(3)
    print(i, ':', kurtosis)

kurtosis_value(input=dataset.iloc[:, 1:7])

"""**Quick interpretation:**

Since all of the columns has positive skewness, I can imply that the data distribution is skewed to the right.

For addition, most of the columns have a negative kurtosis. This imply that the data is scattered (e.g. not centered in a certain value). Only volume that had a certain value.

The unique case of volume column might be related to seasonal patterns. In a certain business days or months, there are an increase of stocks traded, that are centered to a certain range value. This pattern might be persistent and if soon data visualization confirms such seasonal pattern, this is very likely why.

Before jump to data visualization, I'd like to test whether the data are pure random observations or no. I will use ADF test. Note that we need to interpret as:
> **If the p-value is lower than 0.05, ADF test confirms the data are ''pure random''**. Otherwise there are might exist some patterns.
However, note that this test actually do not test whether the data have any trends/seasonalities. It just say that we have to investigate further if the p-value is higher than 0.05
"""

# Take the columns' name as an array
# Use this array to loop ADF test
dataset_columns = dataset.iloc[:, 1:7].columns

for i in dataset_columns:
  result = adfuller(dataset[i])
  print(i)
  # Specify the float precision of ADF statistic
  print(f'ADF Statistic: {result[0]:.6f}')
  print(f'p-value: {result[1]:.6f}')
  print('==========================')

def millions_formatter(x, position):
  '''
      This function to re-scale the volume value in the x-axis. Since the volume has a vast number,
      standard matplotlib graphics could not display the x-axis as it should. Hence, it needs to
      be rescaled by a million unit.

      This function will return the re-scaled value to be displayed in x-axis as position
  '''
  x_val = int(x/1000000)
  return x_val


def make_a_distribution_plot(input):
  '''
      This function mainly to plot distribution of each columns.
      I state number of rows and columns in the figure directly, so that I didn't need to hard-code each graphics.

      Here, note that there are 2 args on the for loop. Given the axes only accept integer/boolean, while
      I also need each columns' name, I need to zip those two args. Hence, I could throw different values for
      each looping: indexes and columns' name.
  '''
  fig, axes = plt.subplots(nrows=3, ncols=2, figsize=[14, 7])
  fig.subplots_adjust(hspace=0.7)
  axes = axes.ravel()

  for i, j in enumerate(dataset_columns):
    dataset[j].hist(ax=axes[i], grid=False)
    axes[i].set_title(f'Distribution of {j} Prices', fontweight='bold')
    axes[i].set_ylabel('Frequency')
    axes[i].set_xlabel('Value')

  axes[5].xaxis.set_major_formatter(FuncFormatter(millions_formatter))
  axes[5].set_title('Distribution of Volume', fontweight='bold')
  axes[5].set_xlabel('Value (in Million)')

make_a_distribution_plot(input=dataset)

"""**Quick Interpretation**
This explains that prices (open, high, low, close, and adj. close) have a similar behavior. They scattered at 5-15 and 25-50. This trully make me curious:
- Do they correlate each other?
- Does this price behavior affect demand (measured by 'volume')?

# Correlation Analysis
"""

price_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close']

# Loop the correlation of 1st column to the ith column
for pc in price_columns:
  correlation = dataset.corr()[pc].sort_values(ascending=False)
  print(correlation)
  print('==========')

# Make a figure for heatmap correlation plot
plt.figure(figsize=(16, 6))

heatmap = sns.heatmap(dataset.corr(), vmin=-1, vmax=1, annot=False,
                      linecolor='white', linewidths=1, center=0)

# Give a title to the heatmap. Pad defines the distance of the title from the top of the heatmap.
heatmap.set_title('Correlation Heatmap', fontsize=30,
                  fontweight='bold', pad=12)

"""**Quick Interpretation**

Using correlation coefficient (visualized by heatmap graphics), the prices really correlate with each other. This is partially shocking, since adj. close price would obviously have a strong correlation with close price. Why? Adj. close is a "product" of close price itself. However, what's shocking is the other price component.

> I would describe the price as a pairing individuals. They are sensitive to each other dynamics. The different is, each price column come from different timeline (hour stamp). Recall the definition of open and close price, while high and low price are somewhere in between open and close price.

> What's happening in open price, would likely play a domino effect to high, low, and close. Also, current open price might be affected by previous open price and might affect future open price.

At the other hand, demand consistently negatively correlate with the price.

This EDA, luckily give me more insights to do descriptive analysis:
> - There are two dynamics that need to be addressed: day-to-day partial price component and in-day price component (dynamics of price components in a day)
- Address shocks or cyclical dynamics

# Descriptive Analysis
"""

def millions_formatter(x, position):
      x_val = int(x/1000000)
      return x_val

def make_line_plot(input):
  '''
      The mechanism of this function is quite same as previous make_a_distribution_plot() function.
      1. It requires two arguments
      2. Re-scale the volume displayed in a specific axis

      The differences are:
      1. Using line plot to display trends
      2. Set additional atributes (lines and areas) to show highlights
  '''
  fig, axes = plt.subplots(nrows=3, ncols=2, figsize=[16, 7])
  fig.subplots_adjust(hspace=0.7)
  axes = axes.ravel()

  for i, j in enumerate(dataset_columns):
    axes[i].plot(input['Date'], input[j])
    axes[i].set_title(f'{j} Fluctuations Over 2004-2016', fontweight='bold')
    axes[i].set_ylabel('Price Value')
    axes[i].set_xlabel('Time')
    axes[i].set_ylim(0, 60)
    axes[i].axvline(input['Date'].loc[input[j].idxmin()],
                  alpha=0.7, color='red')
    axes[i].axvline(input['Date'].loc[input[j].idxmax()],
                  alpha=0.7, color='purple')
    axes[i].axvspan('2007-09-30', '2011-12-25', color='gray', alpha=0.3)

  axes[5].yaxis.set_major_formatter(FuncFormatter(millions_formatter))
  axes[5].set_ylim(0, 1500000000)
  axes[5].set_ylabel('Shares Traded (in Million)')

  return plt.show()

make_line_plot(input=dataset)

"""**Quick Interpretation**
There are four aspect that quite interesting:
- First, shaded area is a place where the price having declining trends, while demand having higher volume.
- Second, lowest price (red line in price component) does not lead to highest demand (purple line in volume).
- Third, highest price (purple line in price component) does not lead to lowest demand (red line in volume).
- Fourth, the start of price decline does not followed by start of demand peak rightaway. It shows that there is a lag of response.

Note that the demand volume is very noisy. Even after the end of shaded area (which the prices started to rise), the demand not consistently show a declining trend (noisy ups and downs)
"""

quartiles = np.percentile(dataset['Volume'], [25, 50, 75])
mu, sig = quartiles[1], 0.74 * (quartiles[2] - quartiles[0])
# Query the dataset value which is NOT in the outside of pre-defined ranges
lesser_noise_dataset = dataset.query(f'(Volume > @mu - 5 * @sig) & (Volume < @mu + 5 * @sig)')

make_line_plot(input=lesser_noise_dataset)

"""Again, after denoising the data, we got the same volume behavior as above. The peak demand does not located where the price is the lowest. Also, demand increases significantly where the price also decline significantly (located somewhere in between 2008 and 2010).

However, note that graphic above does not shows cyclical patterns. Instead, prices' ups and downs kinda happen "randomly". We need to take a closer look for each component.
"""

import matplotlib.pyplot as plt
import pandas as pd

def make_yearly_open_price(input):
'''
      This function wants to zoom-in the line plot to a specific column. In this case, open price column.
      However, I also need to label each line which in i-th year. For addition, I need to make the
      color more aesthetic. Hence, I use color map (packs of colors) and index them to
      label each year.

      For further reading about colormap, this documentation may help you:
      https://matplotlib.org/stable/users/explain/colors/colormaps.html

      I also add addtional description in the graphics, to add more highlights.
'''
  fig, ax = plt.subplots(figsize=[15, 5])
  years = input['Date'].dt.year.unique()
  cmap = plt.get_cmap('tab20b')

  for i, y in enumerate(years):
    yearly_data = input[input['Date'].dt.year == y]
    color = cmap(i / len(years))
    ax.plot(yearly_data['Date'], yearly_data['Open'], label=str(y), color=color)

  ax.set_xlabel('Date')
  ax.set_ylabel('Open Price')
  ax.legend(title='Year',
            frameon=False,
            ncol=2)
  ax.set_ylim(0, 70)
  ax.set_xlim(pd.to_datetime('2003-10-01'), pd.to_datetime('2016-01-01'))
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)

  ax.text(pd.to_datetime('2003-10-01'), 75,
          'Overall Open Price Trends',
          fontdict={'size': 15,
                    'weight': 'bold'})

  ax.text(pd.to_datetime('2003-10-01'), 71,
          'Although Declining Trend and Differ Magnitudes, Open Price Kind of Having Cyclical Patterns Each Month',
          fontdict={'size': 13},
          alpha=0.7)

  return ax

make_yearly_open_price(input=dataset)

def make_yearly_volume(input):
    fig, ax = plt.subplots(figsize=[15, 5])
    years = input['Date'].dt.year.unique()
    cmap = plt.get_cmap('tab20b')

    for i, y in enumerate(years):
        yearly_data = input[input['Date'].dt.year == y]
        color = cmap(i / len(years))
        ax.plot(yearly_data['Date'], yearly_data['Volume'],
                label=str(y), color=color)

    ax.set_xlabel('Date')
    ax.set_ylabel('Volume Stocks Bought')
    ax.legend(title='Year',
              frameon=False,
              ncol=2)
    ax.set_ylim(500, 1400000000)
    ax.set_xlim(pd.to_datetime('2003-10-01'), pd.to_datetime('2016-01-01'))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_major_formatter(FuncFormatter(millions_formatter))

    ax.axvspan('2009-01-01', '2009-12-31', color='gray', alpha=0.3)

    ax.text(pd.to_datetime('2003-10-01'), 1500000000,
            'Overall Volume Trends',
            fontdict={'size': 15,
                      'weight': 'bold'})

    ax.text(pd.to_datetime('2003-10-01'), 1420000000,
            'There is a demand boom circa 2009 and then, slowly but surely, the stock demand decline',
            fontdict={'size': 13},
            alpha=0.7)

    return ax

make_yearly_volume(input=dataset)

"""There are several interesting things:
1. The demand started to decline in the middle of 2009. However, there is a demand boom (again) circa December 2009.
2. Although started to decline, the demand seems increased in the middle of 2011.
3. Even we have a bigger canvas for volume's chart, I barely see a repeated cycle. For example,
> - 2009, 2010, and 2012 have their peaks in first and last year.
  - However, 2013 and 2014 have their peaks in first half of year.
  - In the other hand, 2008 and 2011 have their peaks in last half of year.
  - **It is implied that no clear monthly pattern over years**
4. I assume I need to see a closer look on each year's volume. Such decision will let me to see their monthly behavior.

## Growth Analysis
"""

def make_growth_dataframe(input):
  '''
      This function is iterating two things:
      1. Iterate to calculate growth in each row (for a specified column)
      2. Do such things to other columns

      The results will be stored in a list first and then re-stored as dataframe

      There are several things need to be highlighted:
      1. First rows always result in zero growth (because no previous row),
      2. After filling the first rows with zero value, continue to calculate
      3. To avoid errors because of zero division (which resulted in undefined value),
         I make a try-except Error Handling with specified instruction (append with 0).
         Hence, no unnecessary ZeroDivision-related errors would happen.
      4. There is two main local value:
          a. growth: empty list to be filled with raw growth values
          b. growth_data: transform the empty list to a data set with defined-column names

      The flow of this function:
      1. First, run the function with defined input.
      2. Output of this function (growth_data) stored in an independent variable (growth_dataframe)

      Such flow ease me to further manipulate the growth data (e.g. doing concatenation), since
      variables in this function not stated in global environment.
  '''
  growth_data = pd.DataFrame()  # Create an empty DataFrame
  for column_name in input:
      growth = []  # Define growth list for each column

      for j in range(len(dataset[column_name])):
          if j == 0:
            growth.append(0)
          continue

          try:
              # Calculate growth
              growth_value = (dataset[column_name].iloc[j] - dataset[column_name].iloc[j-1]) / dataset[column_name].iloc[j-1]
              # Scale it to percentages
              growth_percentage = growth_value * 100
              # Limit to two decimals
              growth.append(round(growth_percentage, 2))
          except ZeroDivisionError:
              growth.append(0)

      growth_data[column_name + '_Growth'] = growth  # Add growth values to DataFrame

  return growth_data


growth_dataframe = make_growth_dataframe(input=dataset.iloc[:, 1:7])
# Recursive: the dataset variable will be updated as concatenated values between itself and
# -- growth_dataframe
dataset = pd.concat([dataset, growth_dataframe], axis=1)
dataset

def make_yearly_open_growth(input):
    fig, ax = plt.subplots(figsize=[14, 5])
    years = input['Date'].dt.year.unique()

    for y in years:
        yearly_data = input[input['Date'].dt.year == y]
        ax.plot(yearly_data['Date'], yearly_data['Volume_Growth'], label=str(y))

    ax.set_xlabel('Date')
    ax.set_ylabel('Open Price')
    ax.legend(title='Year',
              ncol=2,
              frameon=False)
    ax.set_ylim(-150, 700)

    return ax

make_yearly_open_growth(input=dataset)

"""## Graphics Customization"""

# Buat data set baru yearly
# Ini menghasilkan semua tahun sih btw
yearly_dataset = {} # Ini datanya kita simpan as hashmap.
input_column = input(str())

def make_a_yearly_dataset(input):
  years = (dataset['Date'].dt.year).unique()

  for y in years:
    yearly_dataset[y] = dataset[['Date', input_column]].loc[dataset['Date'].dt.year == y]

  return yearly_dataset[y]

make_a_yearly_dataset(input=input_column)

# Buat variabel baru untuk per data set baru
# Caveat gede sih kalo mau clone. Jangan di VSCode, RAM mbledos boss
def extract_yearly_data(input):
  for year in range(2004, 2016):
    globals()[f'yearly_{year}_dataset'] = input[year]

  return globals()[f'yearly_{year}_dataset']

extract_yearly_data(input=yearly_dataset)

yearly_2007_dataset

# We need to take a closer look. We could zoom in a certain year (for example, we can specify 2007)

def customize_graph(input):
    fig, ax = plt.subplots(figsize=[14, 5])
    ax.plot(input.iloc[:, 0], input.iloc[:, 1])

    ax.set_xlabel('Date')
    ax.set_ylabel(input.columns[1])
    ax.set_ylim(0, 70)

    # Ambil tahun pertama dari data
    first_year = input['Date'].dt.year.unique()[0]
    ax.set_xlim(pd.Timestamp(f'{first_year}-01-01'), pd.Timestamp(f'{first_year}-12-31'))

    ax.xaxis.set_minor_locator(mpl.dates.MonthLocator(bymonthday=5))
    ax.xaxis.set_major_formatter(plt.NullFormatter())
    ax.xaxis.set_minor_formatter(mpl.dates.DateFormatter('%m-%d'))

    return ax

customize_graph(input=yearly_2006_dataset)
