import os
from pathlib import Path
from typing import List

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from dqfit.dimensions import (Complete, Conformant, Longitudinal, Plausible,
                              Recent)
from dqfit.io import (get_bundle_paths, load_context, read_bundle_resources,
                      read_fhir)
from dqfit.model import Index
from dqfit.transform import transform_to_fhir_path
from dqfit.visualize import draw_population_path_dimensions

PACKAGE_BASE = Path(__file__).parent.absolute()
MAX_CONCURRENCY = int(os.environ.get("MAX_CONCURRENCY", 10))


fhir_base = os.environ.get("FHIR_BASE", f"{PACKAGE_BASE}/data/synthetic")

__all__ = [
    "Index",
    "Conformant",
    "Complete",
    "Plausible",
    "Recent",
    "Longitudinal",
    "transform_to_fhir_path",
    "read_fhir",
    "read_bundle_resources",
    "get_bundle_paths",
    "load_context",
    "draw_population_path_dimensions",
]
