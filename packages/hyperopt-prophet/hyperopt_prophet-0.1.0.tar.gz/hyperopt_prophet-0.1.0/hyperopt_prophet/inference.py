import pickle
from datetime import datetime
from typing import Any, Union

import mlflow
import numpy as np
import pandas as pd


def load_model_from_path(model_path: str) -> Union[None, Any]:
    """
    model_path[str]: The path to the registered model in mlflow
    """
    try:
        loaded_model = mlflow.pyfunc.load_model(model_path)
        model = loaded_model._model_impl.python_model
        return model
    except Exception as e:
        print(e)
        return None


def load_model_from_pkl_path(model_path: str) -> object:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model


def telemetry_inference(
    model_uri: str, dataframe: pd.DataFrame, load_model_type="mlflow_registry"
):
    """
    model_uri[str]: The path to the registered model in mlflow
    dataframe[DataFrame]: Forecast Input of the type {'ds':[timestamp], 'ts_id':[str]}
    Where ts_id is the unique per generation and resembles the id found within the registered model_uri
    """
    try:
        if load_model_type == "pkl":
            print("Loading model from pkl")
            model = load_model_from_pkl_path(model_uri)
        else:
            print("Loading model from mlflow registry")
            model = load_model_from_path(model_uri)
        p_model = model.model(dataframe["ts_id"].values[0])

        inference = p_model.predict(dataframe[["ds", "ts_id"]])
        inference["ts_id"] = dataframe["ts_id"]
        inference["prediction_timestamp"] = datetime.now()

        return inference[
            [
                "ts_id",
                "ds",
                "prediction_timestamp",
                "yhat",
                "yhat_lower",
                "yhat_upper",
                "trend",
                "trend_lower",
                "trend_upper",
            ]
        ]

    except Exception as e:
        print(e)
        return pd.DataFrame(
            columns=[
                "ts_id",
                "ds",
                "prediction_timestamp",
                "yhat",
                "yhat_lower",
                "yhat_upper",
                "trend",
                "trend_lower",
                "trend_upper",
            ]
        )


def get_model_uri(dataframe, pkl_path=None):
    if pkl_path is not None:
        load_model_type = "pkl"
        model_uri = pkl_path
    else:
        load_model_type = "mlflow_registry"
        ts_id = dataframe["ts_id"].head(1).values[0]
        base_model_name = dataframe["base_model_name"].head(1).values[0]
        stage = dataframe["stage"].head(1).values[0]

        model_uri = f"models:/{base_model_name}_{ts_id}/{stage}"
    return model_uri, load_model_type


def load_model_and_generate_prediction(dataframe, pkl_path=None):
    model_uri, load_model_type = get_model_uri(dataframe, pkl_path)
    return telemetry_inference(model_uri, dataframe, load_model_type)


class ProphetInference:
    def __init__(
        self,
        dataframe,
        ts_col="ds",
        id_cols=None,
        value_col="y",
        base_model_name="prophet",
        stage="Production",
        pkl_path=None,
    ):
        if id_cols is None:
            id_cols = ["ts_id"]
        self.dataframe = dataframe
        self.id_cols = id_cols
        self.ts_col = ts_col
        self.value_col = value_col
        self.base_model_name = base_model_name
        self.stage = stage
        self.pkl_path = pkl_path

    def show_model_path(
        self,
    ):
        return get_model_uri(self.create_inference_pdf(), self.pkl_path)[0]

    def create_inference_sdf(self):
        forecast_df = (
            self.dataframe.assign(
                ts_id=lambda df: df[self.id_cols].apply("_".join, axis=1)
            )
            .drop_duplicates(subset=self.id_cols + [self.ts_col])
            .assign(base_model_name=self.base_model_name, stage=self.stage)
        )
        return forecast_df

    def create_inference_pdf(
        self,
    ):
        forecast_df = (
            self.dataframe.assign(
                ts_id=lambda x: x[self.id_cols].apply(lambda x: "_".join(x), axis=1)
            )
            .assign(ds=lambda x: x[self.ts_col])
            .assign(y=lambda x: x[self.value_col])
            .drop_duplicates(self.id_cols + [self.ts_col])
            .assign(base_model_name=lambda x: self.base_model_name)
            .assign(stage=lambda x: self.stage)
        )
        return forecast_df

    def score(
        self,
    ):
        inference_df = self.create_inference_pdf()
        prediction = load_model_and_generate_prediction(inference_df, self.pkl_path)
        prediction_df = pd.merge(
            prediction, inference_df, on=["ts_id", "ds"], how="inner"
        )
        prediction_df["abs_error"] = abs(prediction_df["yhat"] - prediction_df["y"])
        prediction_df["anomaly_flag"] = np.where(
            (prediction_df["y"] > prediction_df["yhat_upper"])
            | (prediction_df["y"] < prediction_df["yhat_lower"]),
            1,
            0,
        )
        return prediction_df
