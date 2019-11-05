
### Project Summary

* This project is an exercise to apply package of dash and plotly to build a dashboard in Python. 
* Inspired by a recent problem I met, computed minimum, maximum, mean and median of large volume of tick data.
* Historical data and tick data for Henry Hub gas price and WTI oil price is collected from Thomson Reuters Refinitiv API using SQL query.
* All source code can be found on my Github page [here](https://github.com/sikunzzz/Python-Dashboard).

### Data collection 
Historical data is available from 2016-11-01 to 2018-10-31, while tick history is available from 2018-10-01 to 2018-12-31.

* Historical Data (daily) of NGc1 and CLc1 collected and saved as json file.
* Three months tick data of NGc1 is collected: each SQL query collects roughly 5 business days of tick data and saved as json files for future use. Saving all tick data in one go is impossible because of the volume of data and the computer will run out of memory.

![data-list](/images/json-list.PNG)

### Dashboard
First let's demonstrate what the dashboard looks like:
![Demo-dashboard1](https://j.gifs.com/XLp3Ao.gif)

![Demo-dashboard2](https://j.gifs.com/6XKk7z.gif)

Returning to our procedures of building the dashboard, after collecting those data, I started to build each component of it.

#### Comparison of historical oil and gas price
The first part is basically a comparison chart of gas and oil price. Historically, oil and gas has strong correlation. This graph plots gas price and 13% of oil price together. A date selector is incorporated to choose the period of data.

#### Monthly mean, median, maximum, minimum of gas price from daily data
The second part is calculation of monthly mean, median, max of gas price for the date selected in the selector.

![hist-gas](/images/historical-gas.PNG)

#### Monthly mean, median, maximum, minimum of gas price from tick data
The third part is to compute monthly min, max mean and median for the tick data. Because of the large volume of data, we can't load the entire month of tick data. For min, max and mean, we need to load tick data of only 5 trading days and compute them respectively. We then find the monthly min, max and mean from our lists. 

For the median，it is trickier, what I have used is a "binning" method. Since I know the minimum and maximum of price and length of the data after the first iteration, I separate the interval between minimum and maximum into equally-spaced bins, e.g if the price is between $3 and $4, I can separate this interval into 10 bins, each of length 0.1. I then go through each data point and determine which bin this data point belong to. After this second iteration of tick data, I will know which bin the median belongs to, so the precision of the median is essentially the width of the bin.

The results for the Oct 2018 median gas price can be plotted in a histogram, here I separated the interval between monthly minimum and monthly maximum into 50 bins.
![median-tick](/images/oct-median.PNG)

Here is also a summary of the statistics calculated for each month of Oct, Nov, Dec in 2018:

![summary-stat](/images/summary-stats.PNG)


#### Daily price movement from tick data
The fourth part is a plot of daily price movement and traded volume using tick data. The problem I currently have for this part is that  it is very slow to plot the new graph, because tick data for one day has huge volume and at the back end, it takes a long time to load the json file.

![tick-gas](/images/tick-gas.PNG)



