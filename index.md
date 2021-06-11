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

Here are some examples of charts, possible patterns that a trader (and hopefully the network) may notice, and their classification.

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

Here is the code to generate data.
```python
def import_data():
    today = dt.datetime(2021, 5, 29)
    start = dt.datetime(2021, 5, 12)
    old_start = dt.datetime(2017, 1, 29)
    chart_end = start + dt.timedelta(days=14)
    end = chart_end + dt.timedelta(days=1)
    # older_assets = {"DOGE-USD", "XMR-USD", "XLM-USD", "LTC-USD", "XEM-USD", "DASH-USD", "ETH-USD"}
    assets = {"ADA-USD", "BNB-USD", "XRP-USD", "DOT1-USD", "UNI3-USD", "BCH-USD", "ETC-USD", "MATIC-USD", "LINK-USD",
              "ALGO-USD", "TRX-USD", "BTT1-USD", "AMP1-USD", "ETH-USD", "MIOTA-USD", "HEX-USD", "SOL1-USD", "VET-USD",
              "THETA-USD", "EOS-USD", "FIL-USD", "XMR-USD", "AAVE-USD", "NEO-USD", "MKR-USD", "BSV-USD", "XTZ-USD",
              "CRO-USD", "ATOM1-USD", "LUNA1-USD", "KSM-USD", "AVAX-USD", "COMP-USD", "ZEC-USD", "HNT1-USD", "CTC1-USD",
              "DCR-USD", "HBAR-USD", "CCXX-USD", "CHZ-USD", "EGLD-USD", "TFUEL-USD", "CEL-USD", "SUSHI-USD",
              "DOGE-USD", "XMR-USD", "XLM-USD", "LTC-USD", "XEM-USD", "DASH-USD"}
    # while end < today:
    while start > old_start:
        for asset in assets:
            print(f"Checking {asset} on {start}")
            try:
                df = pdr.DataReader(asset, 'yahoo', start, end)
                close = df.at[chart_end, 'Close']
                nextclose = df.at[end, 'Close']
                df.drop(df.tail(1).index, inplace=True)
                print(df)
                print(close)
                print(nextclose)
                chart_from_df(df, start, close, nextclose, asset)
            except KeyError:
                continue
            except:  # Need this to be robust against any unexpected errors when running overnight for days
                continue
        start -= dt.timedelta(days=1)
        chart_end -= dt.timedelta(days=1)
        end -= dt.timedelta(days=1)


def chart_from_df(df, date, close, nextclose, asset, filename=None):
    if nextclose is None:
        if filename is None:
            filename = "asset_chart.jpg"
        save = {"fname": filename, "dpi": 60, "bbox_inches": "tight"}
        mplfinance.plot(df, type="candle", style="charles", volume=True, mav=3, axisoff=True, figscale=1, savefig=save)
        return

    change = (nextclose - close) / close
    if not isinstance(change, float):
        return

    if -0.01 < change < 0.01:
        dir = "flat"
    elif 0.01 < change < 0.05:
        dir = "+1%"
    elif 0.05 < change < 0.10:
        dir = "+5%"
    elif change > 0.10:
        dir = "+10%"
    elif -0.01 > change > -0.05:
        dir = "d1%"
    elif -0.05 > change > -0.10:
        dir = "d5%"
    elif change < -0.10:
        dir = "d10%"
    else:
        dir = ""
    num = randint(0, 100)
    if num > 97:
        dataset = "val"
    elif num > 85:
        dataset = "test"
    else:
        dataset = "train"
    filename = f"data/{dataset}/{dir}/{asset}_{date.strftime('%Y-%m-%d')}.jpg"
    print(filename)

    # Make the figure and save it
    save = {"fname": filename, "dpi": 60, "bbox_inches": "tight"}
    mplfinance.plot(df, type="candle", style="charles", volume=True, mav=3, axisoff=True, figscale=1, savefig=save)
```

## Creating the Network

### Code

[All of the final code used for our neural net can be found here.](https://github.com/JohnathonLG/cse455-final/blob/2fbae483b2a8d163912e2d4923bf307f4b4a6158/cse455_final.ipynb)

### Training and Testing Sets

As mentioned before, we were working with images that are 253x357 consistently. We decided to have mild data augmentation for this by padding the edges and taking 253x357 crops out of it. We didn't go for flips or any kind of rotation since that would change the meaning of our charts and we know that the NN will always be fed normal charts for predictions. We set our batch size to 128 and had a training set of 45,099 images and a testing set of 6,511 images.

### Structure

At first, our initial goal was to get a basic convolutional neural network up and running and improving it from there. We began by following the simple convolutional structure from tutorial, consisting of 3 layers with batch normalization. Since our images were considerably larger than those demo'd in tutorial, we decided to make the stride 3 and run it for 30 epochs with a scheduler that reduced the learning rate every 10 epochs (0.1, 0.01, 0.001). 

![initial results](https://github.com/JohnathonLG/cse455-final/blob/38b47f8a6104df95af34e000c8c8ad4d6b64cef9/graphs/30epochs_basenn_stride3.png?raw=true)

As you can see, the result performed very poorly for both the training set and testing set. The losses were too great, so we decided to expand the net to 5 layers and derive our neural net structure from the DarkNet64 structure presented in the tutorial. We lowered the stride to 2, and this network structure also introduced max pooling, which means that we didn't have to deal with weights anymore. At the end there is an adaptive average pool before the fully-connected layer as well, which would help with our odd non-standard image size. We then did a trial run for 5 epochs with the following results.

![second results](https://github.com/JohnathonLG/cse455-final/blob/38b47f8a6104df95af34e000c8c8ad4d6b64cef9/graphs/5epochs_darknet_stride2.png?raw=true)

We thought that iterating this neural net through many more epochs might be the solution. Naively, we set the training to last 80 epochs (with similar scheduling as before except letting each stage run for 20 epochs) and ran it overnight. The performance was not much better than running it for 5 epochs (about 40% and 31% for the training and testing sets respectively). In the end, it was a waste of time and our NN was struggling to even predict our training set correctly.

Because of its poor performance with a more-than-ample training set, we decided to expand the network with more parameters in order to better categorize our complex charts. At first we expanded to 8 layers with a fully-connected layer with 2048 connections but due to runtime concerns, ended up with 7 layers and 1024 connections.

![results](https://github.com/JohnathonLG/cse455-final/blob/38b47f8a6104df95af34e000c8c8ad4d6b64cef9/graphs/morelayers_darknet_60epochs.png?raw=true)

We decided to stick with this structure in the end both due to lack of GPU resources left for us and because optimizing it would take much longer. We recognize that there is an issue of overfitting, but it did end up performing better than when we tried reducing it to 6 layers. Our final NN structure was a 7-layer DarkNet shape trained from scratch.

## Results

### The Numbers and Examples

Overall, we were expecting more success with such a large training set, but our final results are not too bad either. We decided to judge our model based off of its raw accuracy (guessing both polarity and magnitude correctly) and polarity accuracy (guessing if the graph was going to stay/rise/fall correctly).

![Final results](https://github.com/JohnathonLG/cse455-final/blob/38b47f8a6104df95af34e000c8c8ad4d6b64cef9/graphs/final%20results.png?raw=true)

|      | Training set | Testing set |
| ----------- | ----------- | -----------|
| Raw Accuracy    | 99.9%       | 44.9%    |
| Polarity Accuracy (correctly guessing up/down)   | 99.9%       |60.9% |

To further validate that our neural net at least (somewhat) works, we gave it 1 random example from each category that it has never seen before. We then checked to see how close its guess was in terms of polarity and magnitude.

|Currency/Date|Actual Movement | Predicted Movement| Correct Polarity | Correct Magnitude | Candlestick chart |
|---|---|---|---|---|---|
|Bitcoin 2/8/19 | +1-5% | +5-10%| True| False |![+1](https://github.com/JohnathonLG/cse455-final/blob/main/predictions/%2B1/BTC-USD_2019-02-08.jpg?raw=true)|
|Dogecoin 12/3/18 | +5-10% | +5-10% | True | True |![+5](https://github.com/JohnathonLG/cse455-final/blob/38b47f8a6104df95af34e000c8c8ad4d6b64cef9/predictions/+5/DOGE-USD_2018-12-03.jpg?raw=true)|
|Zcash 3/21/20| +10% or more|+10% or more|True|True|![+10](https://github.com/JohnathonLG/cse455-final/blob/38b47f8a6104df95af34e000c8c8ad4d6b64cef9/predictions/+10/ZEC-USD_2020-03-21.jpg?raw=true)|
|Bitcoin SV 4/9/19|no movement|-5-10%|False|False|![n](https://github.com/JohnathonLG/cse455-final/blob/38b47f8a6104df95af34e000c8c8ad4d6b64cef9/predictions/n/BSV-USD_2019-09-04.jpg?raw=true)|
|BitTorrent 1/23/19|-1-5%|-5-10%|True|False|![-1](https://github.com/JohnathonLG/cse455-final/blob/38b47f8a6104df95af34e000c8c8ad4d6b64cef9/predictions/-1/BTT1-USD_2019-01-23.jpg?raw=true)|
|Dash 2/17/21| -5-10% | -1-5%| True| False |![-5](https://github.com/JohnathonLG/cse455-final/blob/38b47f8a6104df95af34e000c8c8ad4d6b64cef9/predictions/-5/-5/DASH-USD_2021-02-17.jpg?raw=true)|
|NEM 3/27/15| -10% or more|-1-5%|True| False | ![-10](https://github.com/JohnathonLG/cse455-final/blob/38b47f8a6104df95af34e000c8c8ad4d6b64cef9/predictions/-10/XEM-USD_2015-03-27.jpg?raw=true)|

We even generated a Bitcoin chart from today (6/9/21) to see what it thinks. Only those reading this will know if it was right or not.

![btctoday](https://github.com/JohnathonLG/cse455-final/blob/38b47f8a6104df95af34e000c8c8ad4d6b64cef9/predictions/unknown/BTC-USD_2021-6-9.jpg?raw=true)
Predicted movement: +1-5%


### Successes
Overall, we feel that the project can be considered a success. We expected the net's ability to guess polarity to be greater than its ability to guess both polarity and magnitude, and we were right. As far as we know, most people who embark on this problem only try to guess a stock's polarity.

- Considering that we are attempting to predict not just the movement direction, but also magnitude, our results are not disappointing. This is a very complex discipline and getting any kind of better-than-random predictions was our goal.
- Generating large amounts of data for an arbitrary list of assets. With more time to run the scraping program, we could have even more data quite easily, which means over a longer period, we feel as if this NN will adjust to more patterns and improve.

### Problems
That said, there are certainly things that either didn't work as planned or should be more carefully considered going forward:

- Many other cryptocurrencies (aka "altcoins") other than Bitcoin tend to follow the movement of Bitcoin. This means that our training set may not have as much organic data as it might appear.
- Overfitting. We're getting an incredibly strong tendency towards overfitting. More weight decay may help, but we need more time to try other network structures, as well.
- Difficulty of the problem. If guessing stocks was easy, programmers would be rich. However, since creating a neural net to predict movement in stocks has a lot of variables (NN parameters/weights/structure, input image parameters, where data is sourced from)  and could end up taking years of research to perfect, we were happy with how our NN did.

## Going Forward
We'd like to continue this project going forward, with more time to experiment and apply the network. We can do this using trading APIs, possibly at
Coinbase. They even support test portfolios, so we could see how the network does without any actual investment (but what's the fun in that?).

Next steps:
- More data. It seems like we could use more data than 45,000 training examples. Additionally, we should add more assets. Should we expand to stocks, or would that hurt the performance in applications with purely cryptocurrencies?
- Try training on and applying the network on different time scales. Maybe these patterns are better indicators when evaluating on shorter time intervals?
- As a more fundamental question, does it makes sense to generate charts and use CNNs compared to simply using the numerical data? Would it learn to extract features as well without generating a candlestick chart first? We chose to take this approach for the project because it mimicks the pattern recognition that we do as traders, but that's not to say it's the only way it could be done with neural networks.

**Thank you for reading!**
