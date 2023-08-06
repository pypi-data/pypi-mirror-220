from enum import Enum


class ExecutionTypes(str, Enum):
    ALL = "all"
    SINGLE = "single"
    UPSTREAM = "upstream"
    DOWNSTREAM = "downstream"


class JobType(str, Enum):
    EXTRACT = "extract"
    PIPELINE = "pipeline"
