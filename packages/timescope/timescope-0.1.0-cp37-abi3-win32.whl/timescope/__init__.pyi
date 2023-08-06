from typing import List, Tuple, Optional, Union
import numpy as np


class TimeSeriesData:
    """
    Models a time series with `time` represented by an array of milliseconds since epoch and `data` represented
    by an array of data point values.

    :param time: Array of timestamps in milliseconds since epoch.
    :param data: Array of data point values.
    :param granularity: Granularity (in milliseconds) of the time series. If no value is provided, the granularity
        is calculated based on the `time` array.
    :param is_step: Whether the time series is a step time series. If no value is provided, the time series is
        considered continuous.
    """
    time: Union[List[int], np.ndarray[int]]
    data: Union[List[float], np.ndarray[float]]
    granularity: Optional[int]
    is_step: Optional[bool]

def cpd_ed_pelt(data: Union[List[float], np.ndarray[float]], min_distance: int) -> List[int]:
    """The ED-PELT algorithm for change point detection.

    The algorithm detects change points in a given array of values, indicating moments when the statistical
    properties of the distribution are changing and the series can be divided into "statistically homogeneous"
    segments. This method supports nonparametric distributions and has an algorithmic complexity of O(N*log(N)).

    This implementation is adapted from a C# implementation created by Andrey Akinshin in 2019 and licensed under the
    MIT License https://opensource.org/licenses/MIT

    :param data: Array of data point values.
    :param min_distance: Minimum distance between change points.
    :return: Returns an array with 1-based indexes of change points. Change points correspond to the end of the
        detected segments. For example, change points for [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2]
        are [6, 12].
    """
    ...

def ssd_cpd(
        time: Union[List[int], np.ndarray[int]],
        data: Union[List[float], np.ndarray[float]],
        min_distance: int,
        var_threshold: float,
        slope_threshold: float
) -> Tuple[List[int], List[float]]:
    """
    Detects steady state behavior in a time series using the ED Pelt change point detection algorithm.

    The time series is split into "statistically homogeneous" segments, and each segment is evaluated based on its
    normalized variance and the slope of the line of best fit. If a segment's variance or slope exceeds the given
    thresholds, it is considered a transient region, otherwise, it is labeled as steady region.

    :param time: Array of timestamps in milliseconds since epoch.
    :param data: Array of data point values.
    :param min_distance: Minimum distance between change points.
    :param var_threshold: The variance threshold for determining steady state regions.
    :param slope_threshold: The slope threshold for determining steady state regions.
    :return: A tuple containing two lists: 1) timestamps; 2) steady state condition
        (0: transient region, 1: steady region) for all timestamps.
    """
    ...

def time_series_resample(time: List[int], data: List[float]) -> Tuple[List[int], List[float]]: ...