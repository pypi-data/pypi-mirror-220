import io
import logging
from typing import List, Optional

import pandas as pd
from PIL import Image
from prophet.plot import plot_plotly

_logger = logging.getLogger(__name__)

logging.getLogger().setLevel(logging.CRITICAL)


def plotly_fig2pil(fig):
    # convert Plotly fig to pil
    fig_bytes = fig.to_image(format="png")
    buf = io.BytesIO(fig_bytes)
    return Image.open(buf)


def get_plotly_forecast(
    model, forecast, changepoints=False, trend=True, figsize=(1200, 600)
):
    return plot_plotly(
        model, forecast, changepoints=changepoints, trend=trend, figsize=figsize
    )


OFFSET_ALIAS_MAP = {
    "W": "W",
    "d": "D",
    "D": "D",
    "days": "D",
    "day": "D",
    "hours": "H",
    "hour": "H",
    "hr": "H",
    "h": "H",
    "H": "H",
    "m": "min",
    "minute": "min",
    "min": "min",
    "minutes": "min",
    "T": "min",
    "S": "S",
    "seconds": "S",
    "sec": "S",
    "second": "S",
}


def get_validation_horizon(df: pd.DataFrame, horizon: int, unit: str) -> int:
    """
    Return validation_horizon, which is the lesser of `horizon` and one quarter of the dataframe's timedelta
    Since the seasonality period is never more than half of the dataframe's timedelta,
    there is no case where seasonality would affect the validation horizon. (This is prophet's default seasonality
    behavior, and we enforce it for ARIMA.)
    :param df: pd.DataFrame of the historical data
    :param horizon: int number of time into the future for forecasting
    :param unit: frequency unit of the time series, which must be a pandas offset alias
    :return: horizon used for validation, in terms of the input `unit`
    """
    MIN_HORIZONS = 4  # minimum number of horizons in the dataframe
    df_timedelta = df["ds"].max() - df["ds"].min()
    horizon_timedelta = pd.to_timedelta(horizon, unit=unit)  # type: ignore

    if MIN_HORIZONS * horizon_timedelta <= df_timedelta:
        return horizon
    validation_horizon_timedelta = df_timedelta / MIN_HORIZONS
    validation_horizon = validation_horizon_timedelta // pd.to_timedelta(1, unit=unit)  # type: ignore
    _logger.info(
        f"Horizon {horizon_timedelta} too long relative to dataframe's timedelta. Validation horizon will be reduced to {validation_horizon_timedelta}."
    )
    return validation_horizon


def generate_cutoffs(
    df: pd.DataFrame,
    horizon: int,
    unit: str,
    num_folds: int,
    seasonal_period: int = 0,
    seasonal_unit: Optional[str] = None,
) -> List[pd.Timestamp]:
    """
    Generate cutoff times for cross validation with the control of number of folds.
    :param df: pd.DataFrame of the historical data.
    :param horizon: int number of time into the future for forecasting.
    :param unit: frequency unit of the time series, which must be a pandas offset alias.
    :param num_folds: int number of cutoffs for cross validation.
    :param seasonal_period: length of the seasonality period.
    :param seasonal_unit: Optional frequency unit for the seasonal period. If not specified, the function will use
                          the same frequency unit as the time series.
    :return: list of pd.Timestamp cutoffs for cross-validation.
    """
    period = max(0.5 * horizon, 1)  # avoid empty cutoff buckets
    period_timedelta = pd.to_timedelta(period, unit=unit)  # type: ignore
    horizon_timedelta = pd.to_timedelta(horizon, unit=unit)  # type: ignore

    if not seasonal_unit:
        seasonal_unit = unit
    seasonality_timedelta = pd.to_timedelta(seasonal_period, unit=seasonal_unit)  # type: ignore

    initial = max(3 * horizon_timedelta, seasonality_timedelta)

    # Last cutoff is "latest date in data - horizon_timedelta" date
    cutoff = df["ds"].max() - horizon_timedelta
    if cutoff < df["ds"].min():
        raise ValueError("Less data than horizon.")
    result = [cutoff]
    while result[-1] >= min(df["ds"]) + initial and len(result) <= num_folds:
        cutoff -= period_timedelta
        # If data does not exist in data range (cutoff, cutoff + horizon_timedelta]
        # Next cutoff point is "last date before cutoff in data - horizon_timedelta"
        if (
            not (((df["ds"] > cutoff) & (df["ds"] <= cutoff + horizon_timedelta)).any())
            and cutoff > df["ds"].min()
        ):
            closest_date = df[df["ds"] <= cutoff].max()["ds"]
            cutoff = closest_date - horizon_timedelta
        # else no data left, leave cutoff as is, it will be dropped.
        result.append(cutoff)
    result = result[:-1]
    if len(result) == 0:
        raise ValueError(
            "Less data than horizon after initial window. Make horizon shorter."
        )
    return list(reversed(result))
