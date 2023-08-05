from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

import pandas as pd
import plotly.express as px
from tqdm import tqdm

import dqfit as dq
from dqfit.dimensions import Complete, Conformant, Plausible, Recent
from dqfit.io import load_context
from dqfit.transform import transform_to_fhir_path


class Index:
    ## starting to emulate openai.Completion.create(model="") syntax

    def create(model: str, context: str):
        if model == "dqi-2":
            return DQIBase(context_key=context, Dimensions=[Conformant, Complete])
        elif model == "dqi-3":
            return DQIBase(
                context_key=context, Dimensions=[Conformant, Complete, Plausible]
            )
        elif model == "dqi-4":
            return DQIBase(
                context_key=context,
                Dimensions=[Conformant, Complete, Plausible, Recent],
            )


class DQIBase(ABC):
    def __init__(
        self,
        context_key: str,
        Dimensions: list = [Conformant],
    ) -> None:
        self.context_key = context_key
        self.context = load_context(context_key)
        self.Dimensions = Dimensions  # Model Dimensions
        self.M = Dimensions  # Model Dimensions
        self.m = pd.DataFrame(self.context["dim"])  # Context Dimensions

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def M_KEYS(self):
        return [dim.__name__ for dim in self.M]

    @property
    def shape(self):
        """
        (Patient x Resource x Path) x (Context Dimensions x Model Dimensions)
        ::
        (organism x molecule x atom) x (context x model)
        """
        return (
            (
                self.result["n"].max(),
                self.result["m"].max(),
            ),
            (len(self.m), len(self.M)),  # weight
        )

    @property
    def path_level(self):
        return self.fhir_path

    def row_score(self, row):
        return (row[self.M_KEYS] * row["W"]).sum()

    def fit(self, fhir_resources: List[dict]):
        """
        Emulates sklearn fit method.
        1. Takes in a list of FHIR resources
        2. Transforms into FHIR Path
        3. Fits each Model Dimension
        4. Aggregates Patient Level Scores
        5. Returns Results DataFrame of shape (m, M)
        """
        if len(fhir_resources) < 1:
            ## consider revisiting support for null resources
            self.fhir_path = pd.DataFrame({"path": []})
            return self.fhir_path
        fhir_path = transform_to_fhir_path(fhir_resources=fhir_resources)
        for Dim in self.Dimensions:
            fhir_path = Dim.fit(fhir_path, self.context)
        fhir_path = fhir_path.query("Conformant == 1").reset_index(drop=True)
        self.fhir_path = fhir_path  # for patient level results

        ## consider handling this in the get_patient_level_score method
        frequencies = (
            fhir_path.groupby(["path"])
            .agg(
                n=("patient_id", "nunique"),
                m=("path", "count"),
            )
            .reset_index()
        )
        frequencies = frequencies.merge(self.m, on="path", how="outer").fillna(0)

        # patient level results
        self.patient_ids = fhir_path["patient_id"].unique()
        patient_level = pd.concat(
            [
                self.get_patient_level_result(patient_id)
                for patient_id in self.patient_ids  # can this turn off?
                # for patient_id in tqdm(self.patient_ids) # can this turn off?
            ]
        )

        self.patient_level = patient_level
        self.patient_level["Score"] = self.patient_level.apply(self.row_score, axis=1)
        self.patient_scores = (
            self.patient_level.groupby("patient_id")
            .agg(Score=("Score", "sum"))
            .sort_values("Score")
            .reset_index()
        )

        result = (
            patient_level.groupby("path")
            .agg({dim.__name__: dim.agg_fn() for dim in self.Dimensions})
            .reset_index()
        )

        result = frequencies.merge(result, on="path", how="left")
        result["Score"] = result.apply(self.row_score, axis=1)

        self.result = result

        return result

    @property
    def index(self):
        return round(self.result["Score"].sum(), 1)

    def get_patient_level_result(self, patient_id: str):
        assert self.fhir_path is not None
        # consider moving to polars for memory efficiency
        patient_level_result = (
            (
                self.fhir_path.query(f"patient_id == '{patient_id}'")
                .groupby("path")
                .agg(
                    {dim.__name__: dim.agg_fn() for dim in self.Dimensions}
                )  # max for Recent
            )
            .reset_index()
            .merge(self.m, how="right", left_on="path", right_on="path")
            .fillna(0)
        )
        patient_level_result.insert(0, "patient_id", patient_id)
        return patient_level_result

    def visualize(self):
        # todo, make order consistent for facet_col, etc such that comparison is apples to apples
        df = self.result.copy()
        df["resourceType"] = df["path"].apply(lambda x: x.split(".")[0])
        dft = df.melt(
            id_vars=["path", "W", "resourceType"],
            var_name="Dimension",
            value_vars=self.M_KEYS,
            value_name="score",
        )
        dft["Dimension"] = pd.Categorical(
            dft["Dimension"], categories=self.M_KEYS, ordered=True
        )
        dft = dft.sort_values(["Dimension", "path"], ascending=True)
        return px.scatter(
            dft,
            x="score",
            y="path",
            facet_col="Dimension",
            color="resourceType",
            size="W",
            size_max=10,
            title=f"DQI-{len(self.M)} | {self.context_key} | Index: {self.index} <sup><br>{self.shape} | (Patient x Path), (ContextDimension, ModelDimension, W)",
            height=600,
        )


