from typing import Optional, Dict

from datazone.models.common import ExecutionTypes
from datazone.service_callers.base import BaseServiceCaller


class JobServiceCaller(BaseServiceCaller):
    service_name = "job"

    @classmethod
    def get_repository_execution_history(cls, repository_id: str):
        session = cls.get_session()
        response = session.get(f"{cls.get_service_url()}/execution/repository/history/{repository_id}")
        return response.json()

    @classmethod
    def get_extract_execution_history(cls, extract_id: str):
        session = cls.get_session()
        response = session.get(f"{cls.get_service_url()}/execution/extract/history/{extract_id}")
        return response.json()

    @classmethod
    def get_execution_logs(cls, execution_id: str, cursor: Optional[str] = None):
        params: Dict = {"cursor": cursor} if cursor else {}

        session = cls.get_session()
        response = session.get(
            f"{cls.get_service_url()}/execution/logs/{execution_id}",
            params=params,
        )
        return response.json()

    @classmethod
    def get_execution_status(cls, execution_id: str):
        session = cls.get_session()
        response = session.get(f"{cls.get_service_url()}/execution/status/{execution_id}")
        return response.json()

    @classmethod
    def run_execution_pipeline(
        cls,
        pipeline_id: str,
        transform_selection: Optional[str],
        execution_type: Optional[ExecutionTypes] = None,
    ):
        body = {}
        if transform_selection is not None and execution_type is not None:
            body.update(
                {
                    "transform_selection": transform_selection,
                    "execution_type": execution_type,
                },
            )

        session = cls.get_session()
        response = session.post(
            f"{cls.get_service_url()}/execution/pipeline/{pipeline_id}",
            json=body,
        )
        return response.json()

    @classmethod
    def inspect_repository(cls, repository_id: str):
        session = cls.get_session()
        response = session.get(
            f"{cls.get_service_url()}/inspect/repository/{repository_id}",
        )
        return response.json()

    @classmethod
    def get_repository_summary(cls, repository_id: str):
        session = cls.get_session()
        response = session.get(
            f"{cls.get_service_url()}/pipeline/summary/{repository_id}",
        )
        return response.json()

    @classmethod
    def run_execution_extract(cls, extract_id: str):
        session = cls.get_session()
        response = session.post(f"{cls.get_service_url()}/execution/extract/{extract_id}")
        return response.json()

    @classmethod
    def redeploy_extract(cls, extract_id: str):
        session = cls.get_session()
        response = session.get(f"{cls.get_service_url()}/extract/deploy/{extract_id}")
        return response.json()
