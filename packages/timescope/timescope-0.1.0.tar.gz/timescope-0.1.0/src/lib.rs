mod detect;
mod utils;
mod sample_data;

use pyo3::prelude::*;
use crate::utils::{TimeSeriesData, calculate_delta_time};
use crate::detect::{EdPelt, SteadyStateDetector};


/// Models a time series with `time` represented by an array of milliseconds since epoch and `data`
/// represented by an array of data point values.
///
/// # Arguments
/// * `time` (Union[List[int], np.ndarray[int]]) - Array of timestamps in milliseconds since epoch.
/// * `data` (Union[List[float], np.ndarray[float]]) - Array of data point values.
/// * `granularity` (Optional[int]) - Granularity (in milliseconds) of the time series. If no value
/// is provided, the granularity is calculated based on the `time` array.
/// * `is_step` (Optional[bool]) - Whether the time series is a step time series. If no value is
/// provided, the time series is considered continuous.
#[derive(Clone)]
#[pyclass(name = "TimeSeriesData")]
struct TimeSeriesDataPy {
    #[pyo3(get)]
    time: Vec<i64>,
    #[pyo3(get)]
    data: Vec<f64>,
    #[pyo3(get)]
    granularity: Option<i64>,
    #[pyo3(get)]
    is_step: Option<bool>
}

#[pymethods]
impl TimeSeriesDataPy {
    #[new]
    fn init(
        time: Vec<i64>, data: Vec<f64>, granularity: Option<i64>, is_step: Option<bool>
    ) -> Self {
        let granularity = granularity.unwrap_or(
            calculate_delta_time(&time)
        );
        let is_step = is_step.unwrap_or(false);
        let ts = TimeSeriesData::new(time, data, granularity, is_step);
        let ts: TimeSeriesDataPy = ts.into();
        ts
    }
    /// Resamples the time series into an equally spaced time series.
    /// # Arguments
    /// * `start_time (Optional[int])` - Defines the start time of the resampled array.
    /// * `end_time (Optional[int])` - Defines the end time of the resampled array.
    /// * `granularity (Optional[int])` - Defines the granularity (in milliseconds) of the resampled
    /// array.
    /// # Returns
    /// * `(TimeSeriesData)` Resampled time series.
    fn equally_spaced_resampling(
        &self,
        start_time: Option<i64>,
        end_time: Option<i64>,
        granularity: Option<i64>
    ) -> TimeSeriesDataPy {
        let ts: TimeSeriesData = self.clone().into();
        let resampled_ts: TimeSeriesDataPy = ts.equally_spaced_resampling(
            start_time,
            end_time,
            granularity
        ).into();
        resampled_ts
    }
    /// Slices the time series according to the provided boundaries.
    /// # Arguments
    /// * `start_time` (int) - Defines the start time of the sliced array.
    /// * `end_time` (int) - Defines the end time of the sliced array.
    /// # Returns
    /// * (TimeSeriesData) Sliced time series.
    fn slice(&self, start_time: i64, end_time: i64) -> TimeSeriesDataPy {
        let ts: TimeSeriesData = self.clone().into();
        let sliced_ts: TimeSeriesDataPy = ts.slice(start_time, end_time).into();
        sliced_ts
    }
    fn __repr__(&self) -> String {
        let n = &self.time.len();
        let time_display: String;
        let data_display: String;
        if n < &5 {
            time_display = self.time.iter()
                    .map(|x| x.to_string())
                    .collect::<Vec<String>>()
                    .join(", ");
            data_display = self.data.iter()
                    .map(|x| x.to_string())
                    .collect::<Vec<String>>()
                    .join(", ");
        } else {
            time_display = format!(
                "{}, {}, ..., {}, {}",
                &self.time[0], &self.time[1], &self.time[n-2], &self.time[n-1]
            );
            data_display = format!(
                "{}, {}, ..., {}, {}",
                &self.data[0], &self.data[1], &self.data[n-2], &self.data[n-1]
            );
        }
        format!(
            "TimeSeriesData(time=[{}], data=[{}], granularity={}, is_step={})",
            time_display,
            data_display,
            self.granularity.unwrap(),
            self.is_step.unwrap()
        )
    }
    fn __str__(&self) -> String {
        self.__repr__()
    }
}

impl From<TimeSeriesDataPy> for TimeSeriesData {
    fn from(value: TimeSeriesDataPy) -> Self {
        TimeSeriesData::new(
            value.time,
            value.data,
            value.granularity.unwrap(),
            value.is_step.unwrap()
        )
    }
}

impl From<TimeSeriesData> for TimeSeriesDataPy {
    fn from(value: TimeSeriesData) -> Self {
        TimeSeriesDataPy {
            time: value.time,
            data: value.data,
            granularity: Some(value.granularity),
            is_step: Some(value.is_step)
        }
    }
}

/// The ED-PELT algorithm for change point detection.
///
/// The algorithm detects change points in a given array of values, indicating moments when the
/// statistical properties of the distribution are changing and the series can be divided into
/// "statistically homogeneous" segments. This method supports nonparametric distributions and has
/// an algorithmic complexity of O(N*log(N)).
///
/// This implementation is adapted from a C# implementation created by Andrey Akinshin in 2019 and
/// licensed under the MIT License https://opensource.org/licenses/MIT
///
/// # Arguments
/// * `data` (Union[List[float], np.ndarray[float]]) - Array of data point values.
/// * `min_distance` (int) - Minimum distance between change points.
///
/// # Returns
/// (List[int]) Array with 1-based indexes of change points. Change points correspond to the end of
/// the detected segments. For example, change points for
/// [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2] are [6, 12].
#[pyfunction]
#[pyo3(text_signature = "(data: Union[List[float], np.ndarray[float]], min_distance: int)")]
fn cpd_ed_pelt(data: Vec<f64>, min_distance: usize) -> PyResult<Vec<i64>> {
    let cpd = EdPelt::new();
    let cp = cpd.get_change_point_indexes(&data, &min_distance);
    Ok(cp)
}

/// Detects steady state behavior in a time series using the ED Pelt change point detection
/// algorithm.
///
/// The time series is split into "statistically homogeneous" segments, and each segment is
/// evaluated based on its normalized variance and the slope of the line of best fit. If a segment's
/// variance or slope exceeds the given thresholds, it is considered a transient region, otherwise,
/// it is labeled as steady region.
///
/// # Arguments
/// * `time_series` (TimeSeriesData) - TimeSeriesData object.
/// * `min_distance` (int) - Minimum distance between change points.
/// * `var_threshold` (float) - The variance threshold for determining steady state regions.
/// * `slope_threshold` (float) - The slope threshold for determining steady state regions.
///
/// # Returns
/// (TimeSeriesData) TimeSeriesData object with the steady state condition (0: transient region, 1:
/// steady region) for all timestamps.
#[pyfunction]
#[pyo3(text_signature = "(time_series: TimeSeriesData, min_distance: int, var_threshold: float, slope_threshold: float)")]
fn ssd_cpd(
    time_series: TimeSeriesDataPy,
    min_distance: usize,
    var_threshold: f64,
    slope_threshold: f64
) -> PyResult<TimeSeriesDataPy> {
    let time_series: TimeSeriesData = time_series.into();
    let ssd = SteadyStateDetector::new();
    let ssd_map = ssd.get_steady_state_status(
        &time_series, &min_distance, &var_threshold, &slope_threshold);
    let ssd_map: TimeSeriesDataPy = ssd_map.into();
    Ok(ssd_map)
}

/// Simple Python library written in Rust for analyzing and scoping out patterns in time series
/// data.
#[pymodule]
fn timescope(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(cpd_ed_pelt, m)?)?;
    m.add_function(wrap_pyfunction!(ssd_cpd, m)?)?;
    m.add_class::<TimeSeriesDataPy>()?;
    Ok(())
}
