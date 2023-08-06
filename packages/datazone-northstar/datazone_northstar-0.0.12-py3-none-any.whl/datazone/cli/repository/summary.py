from rich import print
from rich.console import Console
from rich.table import Table

from datazone.core.common.config import ConfigReader
from datazone.models.config import Config
from datazone.service_callers.job import JobServiceCaller

columns = [
    "Pipeline ID",
    "Pipeline Name",
    "Deploy Status",
    "Transform Name",
    "Function Name",
    "Output Name",
    "Materialized",
    "Dataset ID",
]


def summary() -> None:
    """
    Get summary about project
    """
    config_file = ConfigReader()

    if not config_file.is_config_file_exist():
        print("[bold red]Config file does not exist![/bold red]")
        return

    config: Config = config_file.read_config_file()

    repository_id = str(config.repository_id)
    response_data = JobServiceCaller.get_repository_summary(repository_id=repository_id)

    pipelines = response_data["pipelines"]

    rows = []
    for pipeline in pipelines:
        transforms = pipeline.get("transforms")
        for transform in transforms:
            outputs = transform.get("outputs")
            for output in outputs:
                rows.append(
                    [
                        pipeline["pipeline"]["_id"],
                        pipeline["pipeline"]["name"],
                        pipeline["pipeline"]["deploy_status"],
                        transform["transform"]["name"],
                        transform["transform"]["function_name"],
                        output["name"],
                        str(output["materialized"]),
                        output["dataset_id"],
                    ],
                )

    console = Console()

    table = Table(*columns)
    for row in rows:
        table.add_row(*row)
    console.print(table)
