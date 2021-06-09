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

As an example, here is a chart of Ethereum going parabolic (meaning shooting upwards in price).

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

## Welcome to GitHub Pages

You can use the [editor on GitHub](https://github.com/JohnathonLG/cse455-final/edit/gh-pages/index.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/JohnathonLG/cse455-final/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
