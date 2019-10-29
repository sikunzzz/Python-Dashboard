
# Project Summary

* This project is an exercise to apply package of dash and plotly to visualize data in dashboard in Python. 
* How to compute minimum, maximum, mean and median of large volume of tick data
* Historical data and tick data for Henry Hub gas price and WTI oil price is collected from Thomson Reuter Refinitiv API using SQL query.

### Data collection 
Historical data is available from 2016-11-01 to 2018-10-31, while tick history is available from 2018-10-01 to 2018-12-31.

* Historical Data (daily): NGc1 and CLc1 collected and saved as json file.
* Three months tick data of NGc1 is collected: each SQL query collects roughly 5 business days of tick data and saved as json files for future use. Saving all tick data in one go is impossible because of the volume of data and the computer will run out of memory.

![data-list](/images/json-list.PNG)

### Dashboard
First let's demonstrate what the final produced dashboard look like:
![Demo-dashboard](https://www.youtube.com/watch?v=732R3ccmheQ)

Returning to our procedures, after collecting those data, I started to build components of the dashboard.

#### Comparison of Historical Oil and Gas price
The first part is basically a comparison chart of gas and oil price. Historically, oil and gas has strong correlation. This graph plots gas price and 13% of oil price together. A date selector is incorporated to choose the period of data

#### Monthly mean, median, maximum, minimum of gas price from daily data
The second part is calculation of monthly mean, median, max of gas price for the date selected in the selector.

![hist-gas](/images/historical-gas.PNG)

#### Monthly mean, median, maximum, minimum of gas price from tick data
The third part is to compute monthly min, max mean and median for the tick data. Because of the large volume of data, we can't load the entire month of tick data, so for min and max, we need to load tick data of 5 days and compute their respectively min, max and mean. We then find the monthly min, max and mean. 

For the median is more trickier, what I have used is a "binning" method. Since I know the minimum and maximum of price and length of the data after the first iteration, I separate the interval between minimum and maximum into equally-spaced bins, e.g if the price is between $3 and $4, I can separate this interval into 10 bins, each of length 0.1. I then go through each data point and determine which bin this data point belong to. After this second iteration of tick data, I will know which bin the median belongs to, so the precision of the median is essentially the width of the bin.

The results can for the Oct 2018 median gas price can be plotted in a histogram:
![median-tick](/images/oct-median.PNG)

Here is also a summary of the statistics calculated for Oct, Nov, Dec of 2018

![summary-stat](/images/summary-stats.PNG)


#### Daily price movement from tick data
The fourth part is plot of daily price movement and traded volume using tick data. The problem I currently have for this part is that there it is very slow to plot the new graph, beacause tick data for one day has huge volume and at the back end, it takes a long time to load the json file.

![tick-gas](/images/tick-gas.PNG)



