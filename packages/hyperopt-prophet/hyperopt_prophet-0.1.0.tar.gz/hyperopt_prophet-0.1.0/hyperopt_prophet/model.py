from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union

import cloudpickle
import mlflow
import pandas as pd
import prophet
from mlflow.exceptions import MlflowException
from mlflow.models.signature import ModelSignature, infer_signature
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE
from mlflow.utils.environment import _mlflow_conda_env
from utils import OFFSET_ALIAS_MAP


class ForecastModel(ABC, mlflow.pyfunc.PythonModel):
    @abstractmethod
    def __init__(self):
        super().__init__()

    @property
    @abstractmethod
    def model_env(self):
        pass  # pragma: no cover

    @staticmethod
    def _validate_cols(df: pd.DataFrame, required_cols: List[str]):
        df_cols = set(df.columns)
        required_cols_set = set(required_cols)
        if not required_cols_set.issubset(df_cols):
            raise MlflowException(
                message=(
                    f"Input data columns '{list(df_cols)}' do not contain the required columns '{required_cols}'"
                ),
                error_code=INVALID_PARAMETER_VALUE,
            )

    def infer_signature(self, sample_input: pd.DataFrame = None) -> ModelSignature:  # type: ignore
        signature = infer_signature(
            sample_input, self.predict(context=None, model_input=sample_input)
        )
        return signature


def mlflow_forecast_log_model(
    forecast_model: ForecastModel, sample_input: pd.DataFrame = None
) -> None:  # type: ignore
    """
    Log the model to mlflow
    :param forecast_model: Forecast model wrapper
    :param sample_input: sample input Dataframes for model inference
    """
    # log the model without signature if infer_signature is failed.
    try:
        signature = forecast_model.infer_signature(sample_input)
    except Exception:  # noqa
        signature = None
    mlflow.pyfunc.log_model(
        "model",
        conda_env=forecast_model.model_env,
        python_model=forecast_model,
        signature=signature,
    )  # type: ignore


PROPHET_CONDA_ENV = _mlflow_conda_env(
    additional_pip_deps=[
        f"prophet=={prophet.__version__}",
        f"cloudpickle=={cloudpickle.__version__}",
    ]
)


class ProphetModel(ForecastModel):
    """
    Prophet mlflow model wrapper for univariate forecasting.
    """

    def __init__(
        self,
        model_json: Union[Dict[str, str], str],
        horizon: int,
        frequency: str,
        time_col: str,
    ) -> None:
        """
        Initialize the mlflow Python model wrapper for mlflow
        :param model_json: json string of the Prophet model or
        the dictionary of json strings of Prophet model for multi-series forecasting
        :param horizon: Int number of periods to forecast forward.
        :param frequency: the frequency of the time series
        :param time_col: the column name of the time column
        """
        self._model_json = model_json
        self._horizon = horizon
        self._frequency = frequency
        self._time_col = time_col
        super().__init__()

    def load_context(self, context: mlflow.pyfunc.model.PythonModelContext) -> None:  # type: ignore
        """
        Loads artifacts from the specified :class:`~PythonModelContext` that can be used
        :param context: A :class:`~PythonModelContext` instance containing artifacts that the model
                        can use to perform inference.
        """
        from prophet import Prophet  # noqa: F401

        return

    @property
    def model_env(self):
        return PROPHET_CONDA_ENV

    def model(self) -> prophet.forecaster.Prophet:  # type: ignore
        """
        Deserialize a Prophet model from json string
        :return: Prophet model
        """
        from prophet.serialize import model_from_json

        return model_from_json(self._model_json)

    def _make_future_dataframe(
        self, horizon: int, include_history: bool = True
    ) -> pd.DataFrame:
        """
        Generate future dataframe by calling the API from prophet
        :param horizon: Int number of periods to forecast forward.
        :param include_history: Boolean to include the historical dates in the data
            frame for predictions.
        :return: pd.Dataframe that extends forward from the end of self.history for the
        requested number of periods.
        """
        return self.model().make_future_dataframe(
            periods=horizon,
            freq=OFFSET_ALIAS_MAP[self._frequency],
            include_history=include_history,
        )

    def _predict_impl(self, horizon: int = None, include_history: bool = True) -> pd.DataFrame:  # type: ignore
        """
        Predict using the API from prophet model.
        :param horizon: Int number of periods to forecast forward.
        :param include_history: Boolean to include the historical dates in the data
            frame for predictions.
        :return: A pd.DataFrame with the forecast components.
        """
        future_pd = self._make_future_dataframe(
            horizon=horizon or self._horizon, include_history=include_history
        )
        return self.model().predict(future_pd)

    def predict_timeseries(self, horizon: int = None, include_history: bool = True) -> pd.DataFrame:  # type: ignore
        """
        Predict using the prophet model.
        :param horizon: Int number of periods to forecast forward.
        :param include_history: Boolean to include the historical dates in the data
            frame for predictions.
        :return: A pd.DataFrame with the forecast components.
        """
        return self._predict_impl(horizon, include_history)

    def predict(self, context: mlflow.pyfunc.model.PythonModelContext, model_input: pd.DataFrame) -> pd.Series:  # type: ignore
        """
        Predict API from mlflow.pyfunc.PythonModel
        :param context: A :class:`~PythonModelContext` instance containing artifacts that the model
                        can use to perform inference.
        :param model_input: Input dataframe
        :return: A pd.DataFrame with the forecast components.
        """
        self._validate_cols(model_input, [self._time_col])
        test_df = pd.DataFrame({"ds": model_input[self._time_col]})
        predict_df = self.model().predict(test_df)
        return predict_df["yhat"]

    def infer_signature(self, sample_input: pd.DataFrame = None) -> ModelSignature:  # type: ignore
        if sample_input is None:
            sample_input = self._make_future_dataframe(horizon=1)
            sample_input.rename(columns={"ds": self._time_col}, inplace=True)
        return super().infer_signature(sample_input)


class MultiSeriesProphetModel(ProphetModel):
    """
    Prophet mlflow model wrapper for multi-series forecasting.
    """

    def __init__(
        self,
        model_json: Dict[str, str],
        timeseries_starts: Dict[str, pd.Timestamp],
        timeseries_end: str,
        horizon: int,
        frequency: str,
        time_col: str,
        id_cols: List[str],
    ) -> None:
        """
        Initialize the mlflow Python model wrapper for mlflow
        :param model_json: the dictionary of json strings of Prophet model for multi-series forecasting
        :param timeseries_starts: the dictionary of pd.Timestamp as the starting time of each time series
        :param timeseries_end: the end time of the time series
        :param horizon: Int number of periods to forecast forward
        :param frequency: the frequency of the time series
        :param time_col: the column name of the time column
        :param id_cols: the column names of the identity columns for multi-series time series
        """
        super().__init__(model_json, horizon, frequency, time_col)
        self._frequency = frequency
        self._timeseries_end = timeseries_end
        self._timeseries_starts = timeseries_starts
        self._id_cols = id_cols

    def model(self, id: str) -> Optional[prophet.forecaster.Prophet]:  # type: ignore
        """
        Deserialize one Prophet model from json string based on the id
        :param id: identity for the Prophet model
        :return: Prophet model
        """
        from prophet.serialize import model_from_json

        if id in self._model_json:
            return model_from_json(self._model_json[id])  # type: ignore
        return None

    def _make_future_dataframe(
        self, id: str, horizon: int, include_history: bool = True
    ) -> pd.DataFrame:
        """
        Generate future dataframe for one model by calling the API from prophet
        :param id: identity for the Prophet model
        :param horizon: Int number of periods to forecast forward
        :param include_history: Boolean to include the historical dates in the data
            frame for predictions.
        :return: pd.Dataframe that extends forward from the end of self.history for the
        requested number of periods.
        """
        end_time = pd.Timestamp(self._timeseries_end)
        if include_history:
            start_time = self._timeseries_starts[id]
        else:
            start_time = end_time + pd.Timedelta(value=1, unit=self._frequency)  # type: ignore

        date_rng = pd.date_range(
            start=start_time,
            end=end_time + pd.Timedelta(value=horizon, unit=self._frequency),  # type: ignore
            freq=OFFSET_ALIAS_MAP[self._frequency],
        )
        return pd.DataFrame(date_rng, columns=["ds"])

    def _predict_impl(self, df: pd.DataFrame, horizon: int = None, include_history: bool = True) -> pd.DataFrame:  # type: ignore
        """
        Predict using the API from prophet model.
        :param df: input dataframe
        :param horizon: Int number of periods to forecast forward.
        :param include_history: Boolean to include the historical dates in the data
            frame for predictions.
        :return: A pd.DataFrame with the forecast components.
        """
        col_id = str(df["ts_id"].iloc[0])
        future_pd = self._make_future_dataframe(
            horizon=horizon or self._horizon, id=col_id, include_history=include_history
        )
        return self.model(col_id).predict(future_pd)  # type: ignore

    def predict_timeseries(self, horizon: int = None, include_history: bool = True) -> pd.DataFrame:  # type: ignore
        """
        Predict using the prophet model.
        :param horizon: Int number of periods to forecast forward.
        :param include_history: Boolean to include the historical dates in the data
            frame for predictions.
        :return: A pd.DataFrame with the forecast components.
        """
        ids = pd.DataFrame(self._model_json.keys(), columns=["ts_id"])  # type: ignore
        return (
            ids.groupby("ts_id")
            .apply(lambda df: self._predict_impl(df, horizon, include_history))
            .reset_index()
        )

    @staticmethod
    def get_reserved_cols() -> List[str]:
        """
        Get the list of reserved columns for prophet.
        :return: List of the reserved column names
        """
        reserved_names = [
            "trend",
            "additive_terms",
            "daily",
            "weekly",
            "yearly",
            "holidays",
            "zeros",
            "extra_regressors_additive",
            "yhat",
            "extra_regressors_multiplicative",
            "multiplicative_terms",
        ]
        rn_l = [n + "_lower" for n in reserved_names]
        rn_u = [n + "_upper" for n in reserved_names]
        reserved_names.extend(rn_l)
        reserved_names.extend(rn_u)
        reserved_names.extend(["y", "cap", "floor", "y_scaled", "cap_scaled"])
        return reserved_names

    def model_predict(self, df: pd.DataFrame, horizon: int = None) -> pd.DataFrame:  # type: ignore
        """
        Predict API used for pandas UDF.
        :param df: Input dataframe.
        :param horizon: Int number of periods to forecast forward.
        :return: A pd.DataFrame with the forecast components.
        """
        forecast_df = self._predict_impl(df, horizon)
        return_cols = self.get_reserved_cols() + ["ds", "ts_id"]
        result_df = pd.DataFrame(columns=return_cols)
        result_df = pd.concat([result_df, forecast_df])
        result_df["ts_id"] = str(df["ts_id"].iloc[0])
        return result_df[return_cols]

    def predict(self, context: mlflow.pyfunc.model.PythonModelContext, model_input: pd.DataFrame) -> pd.Series:  # type: ignore
        """
        Predict API from mlflow.pyfunc.PythonModel
        :param context: A :class:`~PythonModelContext` instance containing artifacts that the model
                        can use to perform inference.
        :param model_input: Input dataframe
        :return: A pd.DataFrame with the forecast components.
        """
        self._validate_cols(model_input, self._id_cols + [self._time_col])
        test_df = model_input.copy()
        test_df["ts_id"] = test_df[self._id_cols].astype(str).agg("-".join, axis=1)
        test_df.rename(columns={self._time_col: "ds"}, inplace=True)

        def model_prediction(df):
            model = self.model(df.name)
            if model:
                predicts = model.predict(df)
                # We have to explicitly assign the ts_id to avoid KeyError when model_input
                # only has one row. For multi-rows model_input, the ts_id will be kept as index
                # after groupby("ts_id").apply(...) and we can retrieve it by reset_index, but
                # for one-row model_input the ts_id is missing from index.
                predicts["ts_id"] = df.name
                return predicts

        predict_df = test_df.groupby("ts_id", group_keys=True).apply(model_prediction).reset_index(drop=True)  # type: ignore
        return_df = test_df.merge(predict_df, how="left", on=["ts_id", "ds"])
        return return_df["yhat"]


def mlflow_prophet_log_model(
    prophet_model: Union[ProphetModel, MultiSeriesProphetModel],
    sample_input: pd.DataFrame = None,
) -> None:  # type: ignore
    """
    Log the model to mlflow
    :param prophet_model: Prophet model wrapper
    :param sample_input: sample input Dataframes for model inference
    """
    mlflow_forecast_log_model(prophet_model, sample_input)


import logging
from abc import ABC
from enum import Enum
from functools import partial
from typing import Any, Dict, List, Optional

import hyperopt
import numpy as np
import pandas as pd
from hyperopt import SparkTrials, Trials, fmin
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
from prophet.serialize import model_to_json
from utils import OFFSET_ALIAS_MAP, generate_cutoffs, get_validation_horizon

logging.getLogger().setLevel(logging.CRITICAL)


class ProphetHyperParams(Enum):
    CHANGEPOINT_PRIOR_SCALE = "changepoint_prior_scale"
    SEASONALITY_PRIOR_SCALE = "seasonality_prior_scale"
    HOLIDAYS_PRIOR_SCALE = "holidays_prior_scale"
    SEASONALITY_MODE = "seasonality_mode"


def _prophet_fit_predict(
    params: Dict[str, Any],
    history_pd: pd.DataFrame,
    horizon: int,
    frequency: str,
    cutoffs: List[pd.Timestamp],
    interval_width: int,
    primary_metric: str,
    country_holidays: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Training function for hyperparameter tuning with hyperopt

    :param params: Input hyperparameters
    :param history_pd: pd.DataFrame containing the history. Must have columns ds (date
            type) and y, the time series
    :param horizon: Forecast horizon_timedelta
    :param frequency: Frequency of the time series
    :param num_folds: Number of folds for cross validation
    :param interval_width: Width of the uncertainty intervals provided for the forecast
    :param primary_metric: Metric that will be optimized across trials
    :param country_holidays: Built-in holidays for the specified country
    :return: Dictionary as the format for hyperopt
    """

    model = Prophet(interval_width=interval_width, **params)
    if country_holidays:
        model.add_country_holidays(country_name=country_holidays)
    model.fit(history_pd, iter=200)

    # Evaluate Metrics
    horizon_timedelta = pd.to_timedelta(horizon, unit=frequency)  # type: ignore
    df_cv = cross_validation(
        model, horizon=horizon_timedelta, cutoffs=cutoffs, disable_tqdm=True
    )  # disable tqdm to make it work with ipykernel and reduce the output size
    df_metrics = performance_metrics(df_cv)

    metrics = df_metrics.mean().drop("horizon").to_dict()  # type: ignore

    return {
        "loss": metrics[primary_metric],
        "metrics": metrics,
        "status": hyperopt.STATUS_OK,
    }


class ProphetHyperoptEstimator(ABC):
    """
    Class to do hyper-parameter tunings for prophet with hyperopt
    """

    SUPPORTED_METRICS = ["mse", "rmse", "mae", "mape", "mdape", "smape", "coverage"]

    def __init__(
        self,
        horizon: int,
        frequency_unit: str,
        metric: str,
        interval_width: int,
        country_holidays: str,
        search_space: Dict[str, Any],
        algo=hyperopt.tpe.suggest,
        num_folds: int = 5,
        max_eval: int = 10,
        trial_timeout: int = None,  # type: ignore
        random_state: int = 0,
        is_parallel: bool = True,
    ) -> None:
        """
        Initialization

        :param horizon: Number of periods to forecast forward
        :param frequency_unit: Frequency of the time series
        :param metric: Metric that will be optimized across trials
        :param interval_width: Width of the uncertainty intervals provided for the forecast
        :param country_holidays: Built-in holidays for the specified country
        :param search_space: Search space for hyperparameter tuning with hyperopt
        :param algo: Search algorithm
        :param num_folds: Number of folds for cross validation
        :param max_eval: Max number of trials generated in hyperopt
        :param trial_timeout: timeout for hyperopt
        :param random_state: random seed for hyperopt
        :param is_parallel: Indicators to decide that whether run hyperopt in parallel
        """
        self._horizon = horizon
        self._frequency_unit = OFFSET_ALIAS_MAP[frequency_unit]
        self._metric = metric
        self._interval_width = interval_width
        self._country_holidays = country_holidays
        self._search_space = search_space
        self._algo = algo
        self._num_folds = num_folds
        self._random_state = np.random.default_rng(random_state)
        self._max_eval = max_eval
        self._timeout = trial_timeout
        self._is_parallel = is_parallel

    def fit(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Fit the Prophet model with hyperparameter tunings
        :param df: pd.DataFrame containing the history. Must have columns ds (date
            type) and y
        :return: DataFrame with model json and metrics in cross validation
        """
        df["ds"] = pd.to_datetime(df["ds"])

        seasonality_mode = ["additive", "multiplicative"]

        validation_horizon = get_validation_horizon(
            df, self._horizon, self._frequency_unit
        )
        cutoffs = generate_cutoffs(
            df.reset_index(drop=True),
            horizon=validation_horizon,
            unit=self._frequency_unit,
            num_folds=self._num_folds,
        )

        train_fn = partial(
            _prophet_fit_predict,
            history_pd=df,
            horizon=validation_horizon,
            frequency=self._frequency_unit,
            cutoffs=cutoffs,
            interval_width=self._interval_width,
            primary_metric=self._metric,
            country_holidays=self._country_holidays,
        )

        if self._is_parallel:
            trials = SparkTrials()  # pragma: no cover
        else:
            trials = Trials()

        best_result = fmin(
            fn=train_fn,
            space=self._search_space,
            algo=self._algo,
            max_evals=self._max_eval,
            trials=trials,
            timeout=self._timeout,
            rstate=self._random_state,
        )

        # Retrain the model with all history data.
        model = Prophet(
            changepoint_prior_scale=best_result.get(ProphetHyperParams.CHANGEPOINT_PRIOR_SCALE.value, 0.05),  # type: ignore
            seasonality_prior_scale=best_result.get(ProphetHyperParams.SEASONALITY_PRIOR_SCALE.value, 10.0),  # type: ignore
            holidays_prior_scale=best_result.get(ProphetHyperParams.HOLIDAYS_PRIOR_SCALE.value, 10.0),  # type: ignore
            seasonality_mode=seasonality_mode[best_result.get(ProphetHyperParams.SEASONALITY_MODE.value, 0)],  # type: ignore
            interval_width=self._interval_width,
        )

        if self._country_holidays:
            model.add_country_holidays(country_name=self._country_holidays)

        model.fit(df)

        model_json = model_to_json(model)
        metrics = trials.best_trial["result"]["metrics"]  # type: ignore

        results_pd = pd.DataFrame({"model_json": model_json}, index=[0])
        results_pd.reset_index(level=0, inplace=True)
        for metric in self.SUPPORTED_METRICS:
            if metric in metrics.keys():
                results_pd[metric] = metrics[metric]
            else:
                results_pd[metric] = np.nan
        results_pd["prophet_params"] = str(best_result)

        return results_pd
