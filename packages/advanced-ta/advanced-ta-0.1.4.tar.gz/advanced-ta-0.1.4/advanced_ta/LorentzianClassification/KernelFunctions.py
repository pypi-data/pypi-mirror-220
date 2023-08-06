import math
import pandas as pd


# @function Rational Quadratic Kernel - An infinite sum of Gaussian Kernels of different length scales.
# @param _src <float series> The source series.
# @param _lookback <simple int> The number of bars used for the estimation. This is a sliding value that represents the most recent historical bars.
# @param _relativeWeight <simple float> Relative weighting of time frames. Smaller values resut in a more stretched out curve and larger values will result in a more wiggly curve. As this value approaches zero, the longer time frames will exert more influence on the estimation. As this value approaches infinity, the behavior of the Rational Quadratic Kernel will become identical to the Gaussian kernel.
# @param _startAtBar <simple int> Bar index on which to start regression. The first bars of a chart are often highly volatile, and omission of these initial bars often leads to a better overall fit.
# @returns yhat <float series> The estimated values according to the Rational Quadratic Kernel.
def rationalQuadratic(src: pd.Series, lookback: int, relativeWeight: int, startAtBar: int) -> pd.Series:
    val = pd.Series(0.0, index=src.index)
    for bar_index in range(startAtBar + 1, len(src)):
        currentWeight = 0.0
        cumulativeWeight = 0.0
        for i in range(startAtBar + 2):
            y = src[bar_index-i]
            w = (1 + (i ** 2 / (lookback ** 2 * 2 * relativeWeight))) ** -relativeWeight
            currentWeight += y * w
            cumulativeWeight += w

        val[bar_index] = currentWeight / cumulativeWeight
    return val


# @function Gaussian Kernel - A weighted average of the source series. The weights are determined by the Radial Basis Function (RBF).
# @param _src <float series> The source series.
# @param _lookback <simple int> The number of bars used for the estimation. This is a sliding value that represents the most recent historical bars.
# @param _startAtBar <simple int> Bar index on which to start regression. The first bars of a chart are often highly volatile, and omission of these initial bars often leads to a better overall fit.
# @returns yhat <float series> The estimated values according to the Gaussian Kernel.
def gaussian(src, lookback, startAtBar):
    val = pd.Series(0.0, index=src.index)
    for bar_index in range(startAtBar + 1, len(src)):
        currentWeight = 0.0
        cumulativeWeight = 0.0
        for i in range(startAtBar + 2):
            y = src[bar_index-i]
            w = math.exp(-(i ** 2) / (2 * lookback ** 2))
            currentWeight += y * w
            cumulativeWeight += w

        val[bar_index] = currentWeight / cumulativeWeight
    return val
