from rich.console import Console
from rich.table import Table

from datazone.service_callers.crud import CrudServiceCaller

extract_columns = [
    "ID",
    "Name",
    "Source ID",
    "Dataset ID",
    "Source Table",
    "Mode",
    "Replication Key",
    "Deploy Status",
    "Created At",
    "Created By",
]


def list_func():
    response_data = CrudServiceCaller(service_name="job", entity_name="extract").get_entity_list()

    console = Console()

    table = Table(*extract_columns)
    for datum in response_data:
        values = [
            datum.get("_id"),
            datum.get("name"),
            datum.get("source_id"),
            datum.get("dataset_id"),
            datum.get("source_table"),
            datum.get("mode"),
            datum.get("replication_key"),
            datum.get("deploy_status"),
            datum.get("created_at"),
            datum.get("created_by"),
        ]
        table.add_row(*values)
    console.print(table)
