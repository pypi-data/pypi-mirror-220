from abc import ABC, abstractmethod
from typing import Any, List

import pandas as pd

from dqfit import helpers


class ModelDimension(ABC):
    def __name__(self) -> str:
        return self.__name__

    @staticmethod
    def agg_fn():
        pass

    @staticmethod
    @abstractmethod
    def fit(dim: pd.Series, self):
        pass


class Conformant(ModelDimension):
    @staticmethod
    def agg_fn():
        return "mean"

    @staticmethod
    def fit(fhir_path: pd.DataFrame, context: dict) -> pd.DataFrame:
        # """Takes in fhir_path, returns fhir_path with Conformant vector"""
        context_paths = list(
            pd.DataFrame(context["dim"])["path"]
        )  # just make this np array
        fhir_path["Conformant"] = fhir_path["path"].isin(context_paths).astype(float)
        return fhir_path


class Complete(ModelDimension):
    @staticmethod
    def agg_fn():
        return "mean"

    @staticmethod
    def fit(fhir_path: pd.DataFrame, context: dict) -> pd.DataFrame:
        """Score Conformant paths for Completeness"""

        def _score_dim(dim: pd.Series) -> int:
            # this could use a rethink
            """
            Effective nulls
            """
            value = dim["value"]
            if dim["Conformant"] == 0:
                return None
            elif type(value) == list and len(value) > 0:
                return 1
            elif pd.isna(value):
                return 0
            elif value == {}:
                return 0
            elif value in ["UNK", "unk", "", "unknown"]:
                return 0
            elif len(str(value)) > 0:  # primary case?
                return 1
            else:
                return 0

        fhir_path["Complete"] = fhir_path.query("Conformant == 1").apply(
            _score_dim, axis=1
        )
        return fhir_path


class Plausible(ModelDimension):

    """
    Plausible is a bit more complicated and where I could use the most help

    Idea: I could imagine plausibility models being a fn(research_journal)

    """

    @staticmethod
    def agg_fn():
        return "mean"

    MIN_DATE = "1903-01-01"
    TODAY_ISO = str(pd.to_datetime("today"))[0:10]

    ##
    DATETIME_PATHS = [
        "Procedure.performed[x]",
        "Condition.onset[x]",
        "Condition.abatement[x]",
        "Condition.recordedDate",
        "Patient.birthDate",
        "Observation.effective[x]",
        "MedicationDispense.whenHandedOver",
    ]

    DISCRETE_SETS = {
        "Procedure.status": [
            "preparation",
            "in-progress",
            "not-done",
            "on-hold",
            "stopped",
            "completed",
            "entered-in-error",
            "unknown",
        ],
        "Observation.status": ["final", "registered", "preliminary", "amended"],
        "Patient.gender": ["male", "female", "other", "unknown"],
    }

    # "https://build.fhir.org/valueset-coverage-type.html"

    def period_score(period: dict):
        # DRAFT
        score = 0
        if "start" in period.keys():
            score += Plausible.dt_score(period["start"]) / 2
        if "end" in period.keys():
            yr = int(period["end"][0:4])
            if yr <= 2024:
                score += 0.5
        return score

    def dt_score(dt: str) -> int:
        if pd.isna(dt):
            return 0
        date = dt[0:10]
        if Plausible.MIN_DATE < date <= Plausible.TODAY_ISO:
            return 1
        else:
            return 0

    def discrete_score(fhir_path: str, value: Any) -> int:
        "For in range"
        # this could use a better name
        if value in Plausible.DISCRETE_SETS[fhir_path]:
            return 1
        else:
            return 0

    def codeable_concept_score(codeable_concept, context: dict):
        # {
        #     "coding": [{"system": "http://loinc.org", "code": "4548-4"}]
        # }
        score = 0
        if "coding" not in codeable_concept.keys():
            return score
        # need to upgrade this to new context
        for coding in codeable_concept.get("coding", []):
            if coding["code"] in context["code"]:
                return 1
        return score

    def type_score(type: dict):
        #
        if "coding" in type.keys():
            return 1
        else:
            return 0

    def subject_score(subject: dict, patient_ids: List[str]):
        # print(subject)
        score = 0
        patient_id = (
            subject.get("reference").replace("Patient/", "").replace("urn:uuid:", "")
        )
        if type(subject) != dict:
            return 0
        elif patient_id in patient_ids:
            # referential integrity check
            score += 1
        return score

    def clinical_status_score(clinical_status: dict):
        VALID_CODES = [
            "active",
            "recurrence",
            "relapse",
            "inactive",
            "remission",
            "resolved",
        ]
        score = 0
        if "coding" not in clinical_status.keys():
            return score
        for coding in clinical_status.get("coding", []):
            if coding["code"] in VALID_CODES:
                score += 1
        return score

    def coverage_type_score(clinical_status: dict):
        VALID_CODES = [
            "pay",
            "EHCPOL",
            "HSAPOL",
            "AUTOPOL",
            "COL",
            "UNINSMOT",
            "PUBLICPOL",
            "DENTPRG",
            "DISEASEPRG",
            "CANPRG",
            "ENDRENAL",
            "HIVAIDS",
            "MANDPOL",
            "MENTPRG",
            "SAFNET",
            "SUBPRG",
            "SUBSIDIZ",
            "SUBSIDMC",
            "SUBSUPP",
            "WCBPOL",
            "DENTAL",
            "DISEASE",
            "DRUGPOL",
            "HIP",
            "LTC",
            "MCPOL",
            "POS",
            "HMO",
            "PPO",
            "MENTPOL",
            "SUBPOL",
            "VISPOL",
            "DIS",
            "EWB",
            "FLEXP",
            "LIFE",
            "ANNU",
            "TLIFE",
            "ULIFE",
            "PNC",
            "REI",
            "SURPL",
            "UMBRL",
            "CHAR",
            "CRIME",
            "EAP",
            "GOVEMP",
            "HIRISK",
            "IND",
            "MILITARY",
            "RETIRE",
            "SOCIAL",
            "VET",
        ]
        score = 0
        if "coding" not in clinical_status.keys():
            return score
        for coding in clinical_status.get("coding", []):
            if coding["code"] in VALID_CODES:
                score += 1
        return score

    @staticmethod
    def fit(fhir_path: pd.DataFrame, context: dict) -> pd.DataFrame:
        """Score Conformant paths for Plausibility"""
        patient_ids = fhir_path["patient_id"].unique()

        def _score_dim(dim: pd.Series):
            dim_path = dim["path"]
            value = dim["value"]
            if dim["Complete"] in [None, 0]:
                return 0
            elif dim_path in Plausible.DATETIME_PATHS:
                if type(value) == str:
                    return Plausible.dt_score(value)
                elif type(value) == dict:
                    return Plausible.period_score(value)
            elif dim_path == "patient_id":
                return 1  # todo handle
            elif dim_path.endswith(".clinicalStatus"):
                return Plausible.clinical_status_score(value)
            elif dim_path in Plausible.DISCRETE_SETS.keys():
                return Plausible.discrete_score(dim_path, value)
            elif dim_path.endswith(".code"):
                # todo handle medicationCodeableConcept
                return Plausible.codeable_concept_score(value, context)
            elif dim_path.endswith(".subject"):
                return Plausible.subject_score(subject=value, patient_ids=patient_ids)
            elif dim_path.endswith(".period"):
                return Plausible.period_score(value)
            elif dim_path == "Coverage.type":
                return Plausible.coverage_type_score(value)

        fhir_path["Plausible"] = fhir_path.query("Conformant == 1").apply(
            _score_dim, axis=1
        )
        return fhir_path


class Recent(ModelDimension):
    # THIS IS A DRAFT

    """Recentness of data"""

    @staticmethod
    def agg_fn():
        return "max"

    @staticmethod
    def fit(fhir_path: pd.DataFrame, context: dict) -> pd.DataFrame:
        fhir_path["Date"] = fhir_path.apply(helpers.get_date, axis=1)
        time_horizon = helpers.time_horizon_matrix(
            min_date=context["min_date"], key="Recent"
        )
        fhir_path = fhir_path.merge(time_horizon, on="Date", how="left")
        return fhir_path


class Longitudinal(ModelDimension):

    """Measure of the Longitudinal Range"""

    @staticmethod
    def agg_fn():
        return lambda x: x.max() - x.min()

    @staticmethod
    def fit(path_level: pd.DataFrame, context: dict) -> pd.DataFrame:
        # hm rerun get_date or depend on recent
        path_level["Date"] = path_level.apply(helpers.get_date, axis=1)
        time_horizon = helpers.time_horizon_matrix(
            min_date=context["min_date"], key="Longitudinal"
        )
        path_level = path_level.merge(time_horizon, on="Date", how="left")
        return path_level
