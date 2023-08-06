from enum import IntEnum

# ======================
# ==== Custom Types ====
# ======================

# This section uses PineScript's new Type syntax to define important data structures
# used throughout the script.

class __Config__:
    def __init__(self, **kwargs):
        while kwargs:
            k, v = kwargs.popitem()
            setattr(self, k, v)


class Settings(__Config__):
    source = ""  # Source of the input data
    neighborsCount = 0  # Number of neighbors to consider
    maxBarsBack = 0  # Maximum number of bars to look back for calculations
    featureCount = 0  # Number of features to use for ML predictions
    colorCompression = 0  # Compression factor for adjusting the intensity of the color scale
    showDefaultExits = False  # Default exits occur exactly 4 bars after an entry signal. This corresponds to the predefined length of a trade during the model's training process
    useDynamicExits = False # Dynamic exits attempt to let profits ride by dynamically adjusting the exit threshold based on kernel regression logic


class Feature:
    type: str
    param1: int
    param2: int

    def __init__(self, type, param1, param2):
        self.type = type
        self.param1 = param1
        self.param2 = param2


class FilterSettings(__Config__):
    useVolatilityFilter = False,  # Whether to use the volatility filter
    useRegimeFilter = False,  # Whether to use the trend detection filter
    useAdxFilter = False,  # Whether to use the ADX filter
    regimeThreshold = 0.0,  # Threshold for detecting Trending/Ranging markets
    adxThreshold = 0  # Threshold for detecting Trending/Ranging markets


class Filter(__Config__):
    volatility = False
    regime = False
    adx = False


# Label Object: Used for classifying historical data as training data for the ML Model
class Direction(IntEnum):
    LONG = 1
    SHORT = -1
    NEUTRAL = 0
