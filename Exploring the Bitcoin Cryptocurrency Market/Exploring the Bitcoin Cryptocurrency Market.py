import pandas as pd
import matplotlib.pyplot as plt


dec6 = pd.read_csv('datasets/coinmarketcap_06122017.csv')
# Selecting the 'id' and the 'market_cap_usd' columns
market_cap_raw = dec6[['id', 'market_cap_usd']]
# Counting the number of values
print(market_cap_raw.count())

# Filtering out rows without a market capitalization
cap = market_cap_raw.query('market_cap_usd > 0')
# Counting the number of values again
cap.count()

# Declaring labels for later use in the plots
TOP_CAP_TITLE = 'Top 10 market capitalization'
TOP_CAP_YLABEL = '% of total cap'

# Selecting the first 10 rows and setting the index
cap10 = cap.iloc[:10, :]
cap10.set_index('id', inplace=True)
cap10.head()
# Calculating market_cap_perc
cap10 = cap10.assign(market_cap_perc = lambda x: (x.market_cap_usd/cap.market_cap_usd.sum())*100)
cap10.head()
# Plotting the barplot with the title defined above
ax = cap10.plot.bar(y='market_cap_perc', title="Top 10 market capitalization")
# Annotating the y axis with the label defined above
ax.set_ylabel("% of total cap")
# Colors for the bar plot
COLORS = ['orange', 'green', 'orange', 'cyan', 'cyan', 'blue', 'silver', 'orange', 'red', 'green']
# Plotting market_cap_usd as before but adding the colors and scaling the y-axis
ax = cap10.plot.bar(y='market_cap_usd', color=COLORS, logy=True, title='Top 10 market capitalization')
# Annotating the y axis with 'USD'
ax.set_ylabel("USD")
# Removing the xlabel as it is not very informative
ax.set_xlabel('')
plt.show()

# Selecting the id, percent_change_24h and percent_change_7d columns
volatility = dec6.loc[:, ['id', 'percent_change_24h', 'percent_change_7d']]
# Setting the index to 'id' and dropping all NaN rows
volatility.set_index('id', inplace=True)
volatility = volatility.dropna()
# Sorting the DataFrame by percent_change_24h in ascending order
volatility = volatility.sort_values(by='percent_change_24h')
# Checking the first few rows
volatility.head()


# Defining a function with 2 parameters, the series to plot and the title
def top10_subplot(volatility_series, title):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 6))
    ax = volatility_series[:10].plot.bar(color='darkred', ax=axes[0])
    fig.suptitle(title)
    ax.set_ylabel('% change')
    ax = volatility_series[-10:].plot.bar(color='darkblue', ax=axes[1])
    return fig, ax


DTITLE = "24 hours top losers and winners"
fig, ax = top10_subplot(volatility.percent_change_24h, DTITLE)
plt.show()

# Sorting in ascending order
volatility7d = volatility['percent_change_7d'].sort_values()
WTITLE = "Weekly top losers and winners"
# Calling the top10_subplot function
fig, ax = top10_subplot(volatility7d, WTITLE)
plt.show()
# Selecting everything bigger than 10 billion
largecaps = cap.query('market_cap_usd > 10e+9')
# Printing out largecaps
print(largecaps)


# Making a nice function for counting different marketcaps from the "cap" DataFrame. Returns an int.
def capcount(query_string: str) -> int:
    return cap.query(query_string).count().id


# Labels for the plot
LABELS = ["biggish", "micro", "nano"]
# Using capcount count the cryptos
biggish = capcount('market_cap_usd > 300e+6')
micro = capcount('50e+6 < market_cap_usd < 300e+6')
nano = capcount('market_cap_usd < 50e+6')
# Making a list with the 3 counts
values = [biggish, micro, nano]
# Plotting them with matplotlib
ax = plt.bar(x=LABELS, height=values)
plt.show()
