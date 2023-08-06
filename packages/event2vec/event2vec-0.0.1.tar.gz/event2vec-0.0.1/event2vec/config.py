import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(
    os.getenv(
        "ROOT_DIR", Path(os.path.dirname(os.path.abspath(__file__))) / ".."
    )
)


# PATHS
DIR2DOCS = ROOT_DIR / "docs/source"
DIR2DOCS_STATIC = DIR2DOCS / "_static"

# Default paths
DIR2DATA = ROOT_DIR / "data"
DIR2RESOURCES = DIR2DATA / "resources"
DIR2RESULTS = DIR2DATA / "results"

DIR2TESTS = ROOT_DIR / "tests"
# DIR2TESTS_IMG = ROOT_DIR / "tests" / "img"

PATH2CONCEPTS = DIR2RESOURCES / "MAPPER-SNDS-concept.csv"
PATH2CCAM = DIR2RESOURCES / "ccam_hierarchy.csv"
PATH2ICD10_CHAPTERS = DIR2RESOURCES / "icd10_chapters.csv"
PATH2IR_PHA = DIR2RESOURCES / "IR_PHA_R.csv"

# event models columns
COLNAME_PERSON = "person_id"
COLNAME_STAY_ID = "visit_occurrence_id"
COLNAME_START = "start"
COLNAME_END = "end"
COLNAME_CODE = "event_concept_id"
COLNAME_SOURCE_CODE = "event_source_concept_id"
COLNAME_TYPE = "event_type_concept_id"
COLNAME_SOURCE_TYPE = "event_source_type_concept_id"
COLNAME_QUALIFIER = "qualifier_concept_id"
COLNAME_VALUE = "value"
COLNAME_UNIT = "unit_concept_id"
COLNAME_UNIT_SOURCE = "unit_source_value"
