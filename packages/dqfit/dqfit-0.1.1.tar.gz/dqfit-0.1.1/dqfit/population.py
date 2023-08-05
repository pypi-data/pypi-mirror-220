import json
import sys
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from glob import glob
from time import time

import pandas as pd
import plotly.express as px

import dqfit as dq

def build_population_level_result(
    patient_level: pd.DataFrame, model: str, context_key: str
) -> pd.DataFrame:
    model = dq.Index.create(model=model, context=context_key)

    agg_fn = {
        **{"W": "max", "n": "sum", "m": "sum"},
        **{dim.__name__: dim.agg_fn() for dim in model.Dimensions},
    }

    result = patient_level.groupby("path").agg(agg_fn).reset_index()

    result["Score"] = result.apply(model.row_score, axis=1)
    return result

def process_bundle(bundle_path: str, model: str, context_key: str) -> None:
        model = dq.Index.create(model=model, context=context_key)
        fhir_resources = dq.read_bundle_resources(bundle_path)
        model.fit(fhir_resources)
        return model.result


def build_patient_level_result(model: str, context_key: str, bundle_paths: list):

    main_func = partial(process_bundle, model=model, context_key=context_key)
    with ProcessPoolExecutor(max_workers=dq.MAX_CONCURRENCY) as exec:
        futures = exec.map(main_func, bundle_paths)
    patient_level = pd.concat(list(futures))
    return patient_level


def get_index(result: pd.DataFrame):
    return round(result["Score"].sum(), 1)


def visualize(population_result: pd.DataFrame, model: str, context_key: str):
    model = dq.Index.create(model=model, context=context_key)
    model.result = population_result
    return model.visualize()


if __name__ == "__main__":
    start = time()

    population_key = sys.argv[1]
    model_key = sys.argv[2]
    context_key = sys.argv[3]

    output_base = f"{dq.results_base}/{population_key}/{context_key}"
    patient_level_path = f"{output_base}/patient_level.parquet"
    population_level_path = f"{output_base}/population_level.parquet"
    result_html_path = f"{output_base}/result.html"
    index_path = f"{output_base}/index.json"

    bundle_paths = dq.get_bundle_paths(population_key=population_key)

    # prompt
    print(f"Model: {model_key}")
    print(f"Context: {context_key}")
    print(f"n: {len(bundle_paths)}")

    patient_level = build_patient_level_result(
        model=model_key, context_key=context_key, bundle_paths=bundle_paths
    )

    population_level = build_population_level_result(
        patient_level=patient_level, model=model_key, context_key=context_key
    )

    print(f"\nData Quality Index: {get_index(population_level)}\n")
    print(population_level)

    ## handle output

    result = {
        "Index": get_index(population_level),
        "context": context_key,
        "model": model_key,
        "n": len(bundle_paths),
        "created": int(start),
    }

    patient_level.to_parquet(patient_level_path)
    population_level.to_parquet(population_level_path)
    visualize(population_level, model=model_key, context_key=context_key).write_html(
        result_html_path
    )

    with open(index_path, "w") as f:
        json.dump(result, f)

    print("\nResults available at:")
    print(f"{index_path}")
    print(f"{patient_level_path}")
    print(f"{population_level_path}")
    print(f"\nresult_html: \n{result_html_path}\n")

    print(f"Runtime: {int(time()-start)} seconds")
