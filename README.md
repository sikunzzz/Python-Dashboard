
# Project Summary

I joined a quant competition recently and have 3months access to the financial database of Refinitiv. Before my access right expires, I want to utilize this data and build something related to the data I can get hold of.

This project is an exercise to apply package of dash and plotless to visualize data in dashboard in Python. Historical data and tick data for Henry Hub gas price. Data is collected from Refinitiv API using SQL query.

Historical data is available from 2016-11-01 to 2018-10-31, while tick history is available from 2018-10-01 to 2018-12-31.


### Data collection: 

* Historical Data (daily): NGc1 and CLc1 collected and saved as Jason file.
* 3 months tick data of NGc1 is collected: each SQL query collect roughly 5 business days of tick data and saved as json file for future use, saved all tick data is impossible because of the volume of data and the computer will run out of memory.

### Dashboard

After collecting those data, I started to build components of the dashboard.

* 1. The first part is basically a comparison chart of gas and oil price. Historically, oil and gas has strong correlation. This graph plots gas price and 13% of oil price together. A date selector is incorporated to choose the period of data
* 2. The second part is calculation of monthly mean, median, max of gas price for the date selected in the selector.
* 3. The third part is plot of daily price movement and traded volume using tick data. The problem I currently have for this part is that there it is very slow to plot the new graph, beacause tick data for one day has huge volume and at the back end, it takes a long time to load the json file.

