import gzip
import json
import os
from glob import glob
from pathlib import Path
from typing import List

import dqfit as dq


def get_bundle_paths(population_key: str) -> list:
    print(f"Population: {population_key}")
    if ".csv" in population_key:
        # support loading paths/ids from file
        with open(population_key, "r") as f:
            keys = f.read()
        return [f"{dq.fhir_base}/{k}" for k in keys]

    else:
        # prefix like
        return glob(f"{dq.fhir_base}/{population_key}/*")


def read_bundle_resources(bundle_path: str) -> List[dict]:
    fhir_resources = []

    if bundle_path.endswith(".json.gz"):
        with gzip.open(bundle_path, "rb") as f:
            bundle = json.load(f)
            for entry in bundle["entry"]:
                fhir_resources.append(entry["resource"])
    else:
        with open(bundle_path, "r") as f:
            bundle = json.load(f)
            for entry in bundle["entry"]:
                fhir_resources.append(entry["resource"])

    # assert len(fhir_resources) > 0, f"No FHIR Resources found in {bundle_path}"
    return fhir_resources


def read_fhir(json_dir: str = "path/to/fhir") -> List[dict]:
    """
    A FHIR Resource is a common demoninator between FHIR Bulk Data and FHIR Bundles
    Tradeoff with bulk is that you must load the whole population into memory in order to
    process a Patient Level Score.

    TBD: One memory optimization approach we could take it to tranform.py to Path at runtime
    """
    bulk_paths = glob(f"{json_dir}/*.ndjson")
    bundle_paths = glob(f"{json_dir}/*.json")
    bundle_gz_paths = glob(f"{json_dir}/*.json.gz")

    fhir_resources = []

    if len(bulk_paths) > 0:
        for bulk_path in bulk_paths:
            with open(bulk_path, "r") as f:
                for line in f:
                    fhir_resources.append(json.loads(line))

    if len(bundle_paths) > 0:
        for bundle_path in bundle_paths:
            try:
                with open(bundle_path, "r") as f:
                    bundle = json.load(f)
                    for entry in bundle["entry"]:
                        fhir_resources.append(entry["resource"])
            except Exception as e:
                print(f"Failed to read {bundle_path}: {e}")

    if len(bundle_gz_paths) > 0:
        for bundle_gz_path in bundle_gz_paths:
            try:
                with gzip.open(bundle_gz_path, "rb") as f:
                    bundle = json.load(f)
                    for entry in bundle["entry"]:
                        fhir_resources.append(entry["resource"])
            except Exception as e:
                print(f"Failed to read {bundle_gz_path}: {e}")

    assert len(fhir_resources) > 0, f"No FHIR Resources found in {json_dir}"
    return fhir_resources


def load_context(context_key: str = "COLE") -> dict:
    context_path = f"{dq.PACKAGE_BASE}/data/context/{context_key}.json"
    with open(context_path, "r") as f:
        context = json.load(f)
    return context
