from rich.console import Console
from rich.table import Table

from datazone.service_callers.crud import CrudServiceCaller

source_columns = ["ID", "Name", "Host", "Port", "User", "Type", "Database Name", "Schema Name", "Created At", "Created By"]


def list_func():
    response_data = CrudServiceCaller(service_name="dataset", entity_name="source").get_entity_list()

    console = Console()

    table = Table(*source_columns)
    for datum in response_data:
        values = [
            datum.get("_id"),
            datum.get("name"),
            datum.get("connection_parameters").get("host"),
            datum.get("connection_parameters").get("port"),
            datum.get("connection_parameters").get("user"),
            datum.get("connection_parameters").get("database_type"),
            datum.get("connection_parameters").get("database_name"),
            datum.get("connection_parameters").get("schema_name"),
            datum.get("created_at"),
            datum.get("created_by"),
        ]
        table.add_row(*values)
    console.print(table)
