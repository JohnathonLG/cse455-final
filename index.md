## The Problem

Stock and cryptocurrency traders consider a wide array of information in their work. One of the critical tools in their toolbox is Technical Analysis. This involves analyzing
charts on various time scales, looking for specific patterns. In particular, a common form of price chart is known as a "candlestick" chart, which breaks up the plot into
bars for each time interval (1 min, 5 min, 15 min, 1 hr, 1 day, etc). Each bar indicates the opening price, closing price, max, and min for that interval. The color
of the "body" of the bar indicates the bearish or bullish movement. ("Bearish" and "Bullish" are terms for decreasing and increasing price, respectively.)

![Candlestick Chart](https://assets.cmcmarkets.com/images/candlestick1_small.png)

Additionally, traders consider many other types of data on their plots as well, such as:
- Trading Volume: The amount/value of trading that occurred over the time interval on that particular asset.
- Moving averages: For a clearer view of trends.
- Moving Average Convergence Divergence (MACD): A special type of chart showing the relationship between two different exponential moving averages (EMAs).
- Relative Strength Indicator (RSI): A metric which describes whether an asset is considered "overbought" or "oversold." A similar but subtley different way of showing price momentum.

and many more. In all of these charts, traders seek to identify patterns, which could give hints for future movements. Such patterns can be very common, and very strong
indicators. In fact, they are frequently given names. The inspiration for this project was to see if a Convolutional Neural Network (CNN) could perform the same task,
identifying patterns and predicting short-term movement.

## Generating Data

The primary challenge in tackling this project was creating our own dataset. We first downloaded a CSV of the second-by-second price movemen of Bitcoin since
its inception. However, reformatting this data into acceptable data structures for common chart-plotting libraries proved to be an unnecessary headache.
Furthermore, we wanted to be able to better analyze the market as a whole, rather than one asset. Using `Matplotlib/mplfinance` with Pandas `data_reader`,
we were able to get data for any asset on the database (we used Yahoo finance) on any day.

### Charts
We elected to include 14 days of price data on each chart, using simple red/green candlesticks ("Charles" style), with volume bars on the bottom and a
3-day moving average line plotted on top. To keep things simple for the network, we ommitted any scale/text and exaggerated the bars for easier feature extraction.

As an example, here is a chart of Ethereum going parabolic. (Shooting upwards in price. "Mooning" if you will.)

![Example Chart](https://github.com/JohnathonLG/cse455-final/blob/main/ETH-USD_2017-02-15.jpg?raw=true)

### Classification
Each chart was classified into 7 outcomes, based on the price performance the next day:
- \>10% growth
- \>5% growth
- \>1% growth
- Approximately flat
- \>1% decline
- \>5% decline
- \>10% decline

Here are some examples of charts, possible patterns that a trader may notice (and hopefully the network as well), and their classification.

#### Bullflag / Descending Wedge
Classification: Bullish (+ \>5%)

One of the strongest bullish signals. Recognizable by an overall descending trend, with oscillations of decreasing amplitude, AKA "consolidating,"
ready to "break out" significantly upward. Volume is seen to be following the price movements closely, which can be considered a good sign.

![Bullflag Example](https://github.com/JohnathonLG/cse455-final/blob/main/ETH-USD_2016-04-25.jpg?raw=true)

#### Ascending Wedge / Reversal
Classification: Bearish (- \>5%)

The opposite of the Descending Wedge. Overall an ascending trend, with oscillations diminishing. Typically represents an upcoming reversal, which we can see
at the end of this chart. Inconsistent/uncertain trading volume also makes this a worrisome outlook as well. Volume should ideally be increasing when the price
is increasing.

![Ascending Wedge Example](https://github.com/JohnathonLG/cse455-final/blob/main/DCR-USD_2017-01-21.jpg?raw=true)

#### Pennant
Classification: Bullish (+ \>%5)

Notable for having a sharp uptick in value (the staff) followed by consolidation (the pennant), followed by an upward breakout. High volume is another factor which indicates
the upcoming upward movement. This is a very common pattern in cryptocurrency, which causes an overall "stepwise" pattern during bullish periods.

![Pennant Example](https://github.com/JohnathonLG/cse455-final/blob/main/BTC-USD_2017-11-26.jpg?raw=true)

For the final dataset, we ran the program for several days, gathering data for each asset on each day, classifying it, and randomly saving it to either the train,
test, or validation set. This produced a training set of roughly 45,000, testing set of 6,500, and a validation set of 1,700.

## Creating the Network

## Results

### Successes
Overall, we feel that the project can be considered a success.

- Considering that we are attempting to predict not just the movement direction, but also magnitude, our results are not disappointing.
- Generating large amounts of data for an arbitrary list of assets. With more time to run the scraping program, we could have even more data quite easily.

### Problems
That said, there are certainly things that either didn't work as planned or should be more carefully considered going forward:

- Many other cryptocurrencies (aka "altcoins") other than Bitcoin tend to follow the movement of Bitcoin. This means that our training set may not have as much organic data as it might appear.
- Overfitting. We're getting an incredibly strong tendency towards overfitting. More weight decay may help, but we need more time to try other network structures, as well.

## Going Forward
We'd like to continue this project going forward, with more time to experiment and apply the network. We can do this using trading APIs, possibly at
Coinbase. They even support test portfolios, so we could see how the network does without any actual investment (but what's the fun in that?).

Next steps:
- More data. It seems like we could use more data than 45,000 training examples. Additionally, we should add more assets. Should we expand to stocks, or would that hard the performance in applications with purely cryptocurrencies?
- Try training on and applying the network on different time scales. Maybe these patterns are better indicators when evaluating on shorter time intervals?
- As a more fundamental question, does it makes sense to generate charts and use CNNs compared to simply using the numerical data? Would it learn to extract features as well without generating a candlestick chart first? We chose to take this approach for the project because it mimicks the pattern recognition that we do as traders, but that's not to say it's the only way it could be done with neural networks.

**Thank you for reading!**
