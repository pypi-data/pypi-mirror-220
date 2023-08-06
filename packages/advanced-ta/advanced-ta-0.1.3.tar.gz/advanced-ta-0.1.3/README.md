This module is a python implementation of Lorentzian Classification algorithm developed by @jdehorty in pinescript. The original work can be found here - https://www.tradingview.com/script/WhBzgfDu-Machine-Learning-Lorentzian-Classification/

## Prerequisites
> Ensure that [TA-Lib](https://ta-lib.org/hdr_dw.html) is downloaded and built for your platform. Set `TA_INCLUDE_PATH` and `TA_LIBRARY_PATH` as mentioned in [ta-lib-python](https://github.com/TA-Lib/ta-lib-python#installation). TA-Lib package itself will be installed as a dependency of `advanced-ta`.

## Usage

At the most simplest, you can just do this:
```python
from advanced_ta import LorentzianClassification
.
.
    # df here is the dataframe containing stock data as [['open', 'high', 'low', 'close', 'volume']]. Notice that the column names are in lower case.
    lc = LorentzianClassification(df)
    lc.dump('output/result.csv')
    lc.plot('output/result.jpg')
.
.
```

For advanced use, you can do:
```python
from advanced_ta import LorentzianClassification
import TA-Lib as ta
.
.
    # df here is the dataframe containing stock data as [['open', 'high', 'low', 'close', 'volume']]. Notice that the column names are in lower case.
    lc = LorentzianClassification(
        df,
        features=[
            LorentzianClassification.Feature("RSI", 14, 2),  # f1
            LorentzianClassification.Feature("WT", 10, 11),  # f2
            LorentzianClassification.Feature("CCI", 20, 2),  # f3
            LorentzianClassification.Feature("ADX", 20, 2),  # f4
            LorentzianClassification.Feature("RSI", 9, 2),   # f5
            ta.MFI(df['open'], df['high'], df['low'], df['close'], df['volume']) #f6
        ],
        settings=LorentzianClassification.Settings(
            source='close',
            neighborsCount=8,
            maxBarsBack=2000,
            useDynamicExits=False
        ),
        filterSettings=LorentzianClassification.FilterSettings(
            useVolatilityFilter=True,
            useRegimeFilter=True,
            useAdxFilter=False,
            regimeThreshold=-0.1,
            adxThreshold=20,
            kernelFilter = LorentzianClassification.KernelFilter(
                useKernelSmoothing = False
                lookbackWindow = 8
                relativeWeight = 8.0
                regressionLevel = 25
                crossoverLag = 2
            )
        ))
    lc.dump('output/result.csv')
    lc.plot('output/result.jpg')
.
.
```