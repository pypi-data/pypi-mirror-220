import typer
from rich import print

from datazone.core.common.types import ExtractMode
from datazone.service_callers.crud import CrudServiceCaller


def create(
    name: str = typer.Option(..., prompt=True),
    source_id: str = typer.Option(..., prompt=True),
    source_table: str = typer.Option(..., prompt=True),
    mode: ExtractMode = typer.Option(ExtractMode.OVERWRITE, prompt=True),
):
    payload = {
        "name": name,
        "source_id": source_id,
        "source_table": source_table,
        "mode": mode,
    }

    if mode == "append":
        replication_key = typer.prompt("Replication Key", type=str, default="id")
        payload.update({"replication_key": replication_key})
    # TODO Add source check
    CrudServiceCaller(service_name="job", entity_name="extract").create_entity(payload=payload)

    print("[bold green]Extract has created successfully [/bold green] :tada:")
