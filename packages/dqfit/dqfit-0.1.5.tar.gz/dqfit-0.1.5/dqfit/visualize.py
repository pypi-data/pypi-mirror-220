import pandas as pd
import plotly.express as px

import dqfit as dq


def draw_population_path_dimensions(population_level: pd.DataFrame) -> px.scatter:
    model_dimension_keys = ["Conformant", "Complete", "Plausible"]

    df = population_level.copy()
    df["resourceType"] = df["path"].apply(lambda x: x.split(".")[0])
    dft = df.melt(
        id_vars=["path", "W", "resourceType", "n", "m"],
        var_name="Dimension",
        value_vars=model_dimension_keys,
        value_name="score",
    )
    dft["Dimension"] = pd.Categorical(
        dft["Dimension"], categories=model_dimension_keys, ordered=True
    )
    dft = dft.sort_values(["Dimension", "path"], ascending=True)
    return px.scatter(
        dft,
        x="score",
        y="path",
        facet_col="Dimension",
        color="resourceType",
        size="W",
        hover_data=["n", "m"],
        size_max=10,
        # title=f"DQI-{len(self.M)} | {self.context_key} | Index: {self.index} <sup><br>{self.shape} | (Patient x Path), (ContextDimension, ModelDimension, W)",
        height=600,
    )


def draw_patient_level_distribution(patient_level: pd.DataFrame) -> px.histogram:
    pass
