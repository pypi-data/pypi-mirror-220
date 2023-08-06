from enum import Enum


class DatabaseType(str, Enum):
    MYSQL = "mysql"
    POSTGRES = "postgres"
    ORACLE = "oracle"
    MONGO = "mongo"


class ExtractMode(str, Enum):
    OVERWRITE = "overwrite"
    APPEND = "append"
