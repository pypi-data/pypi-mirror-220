from typing import List
from uuid import UUID

from pydantic import BaseModel, FilePath, Field

from datazone.utils.types import PydanticObjectId


class Pipeline(BaseModel):
    id: PydanticObjectId
    path: FilePath


class Config(BaseModel):
    repository_name: str
    repository_id: UUID
    pipelines: List[Pipeline] = Field(default_factory=list)
