import time

from rich.console import Console
from rich.live import Live
from rich.table import Table

from datazone.service_callers.job import JobServiceCaller

FINISHED_STATUSES = [
    "SUCCESS",
    "FAILURE",
    "CANCELED",
    "UPSTREAM_FAILURE",
]


def fetch_logs(execution_id: str):
    cursor = None
    last_message = None
    while True:
        log_response_data = JobServiceCaller.get_execution_logs(execution_id=execution_id, cursor=cursor)
        status_response_data = JobServiceCaller.get_execution_status(execution_id=execution_id)

        status = status_response_data.get("status")
        cursor = log_response_data.get("cursor")
        new_logs = log_response_data.get("logs", [])
        if new_logs:
            new_last_message = new_logs[-1].get("message")
            if last_message != new_last_message:
                last_message = new_last_message
                yield new_logs
        if status in FINISHED_STATUSES:
            break
        time.sleep(1)


def log(execution_id: str):
    console = Console()
    logs_table = Table(show_header=False, show_edge=False)
    logs_table.add_column()
    logs_table.add_column()
    logs_table.add_column()
    logs_table.add_column()
    logs_table.add_column(style="dim")

    with Live(console=console, screen=False, auto_refresh=False) as live:
        log_generator = fetch_logs(execution_id=execution_id)
        for log_batch in log_generator:
            for log_data in log_batch:
                log_time = log_data["log_time"]
                event_type = log_data.get("event_type", " - ")
                step_key = log_data.get("step_key") or " - "
                logs_table.add_row(
                    "[green]✔[/green]",
                    f"[bold]{log_time}[/bold]",
                    f"[bold]{step_key}[/bold]",
                    f"{event_type}",
                    f"{log_data['message']}",
                )
                live.update(logs_table)
                live.refresh()
