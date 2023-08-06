from typing import Optional

import typer
from rich import print

from datazone.core.common.types import DatabaseType
from datazone.service_callers.crud import CrudServiceCaller


def create():
    # TODO add choice for other source types, like restapi, queue etc.
    source_name = typer.prompt("Source Name", type=str)
    database_type = typer.prompt("Database Type", type=DatabaseType, default=DatabaseType.MYSQL)
    host = typer.prompt("Host", type=str)
    port = typer.prompt("Port", type=str)
    user = typer.prompt("User", type=str)
    password = typer.prompt("Password", hide_input=True, confirmation_prompt=True, type=str)
    database_name = typer.prompt("Database Name", type=str)
    schema_name = typer.prompt("Schema Name", type=Optional[str])

    CrudServiceCaller(service_name="dataset", entity_name="source").create_entity(
        payload={
            "name": source_name,
            "connection_parameters": {
                "source_type": "database",
                "database_type": database_type,
                "host": host,
                "port": port,
                "user": user,
                "password": password,
                "database_name": database_name,
                "schema_name": schema_name,
            },
        },
    )

    # TODO add test connection mechanism
    print("Source has created successfully :tada:")
