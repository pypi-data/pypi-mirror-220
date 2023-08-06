import os
import shutil
from pathlib import Path
from typing import Dict

import git
import typer
from rich import print

from datazone.service_callers.crud import CrudServiceCaller
from datazone.service_callers.git import GitServiceCaller
from datazone.service_callers.repository import RepositoryServiceCaller


def initialize_git_repo(project: Dict) -> None:
    repository_name = project.get("repository_name")
    project_name = project.get("name")

    path = Path(project_name)
    if path.exists():
        delete = typer.confirm(
            f"There is {project_name} folder, it will be truncated. Are you sure?",
        )
        if not delete:
            return

        shutil.rmtree(path)

    os.mkdir(project_name)
    os.chdir(project_name)

    server = RepositoryServiceCaller.get_default_server()
    organisation_name = server.get("default_organisation")

    if not organisation_name:
        print("[bold red]Default organisation does not exist![/bold red]")
        return

    session = RepositoryServiceCaller.create_session(
        server_id=server["_id"],
        organisation_name=organisation_name,
        repository_name=repository_name,
    )
    token = session.get("token")

    git_url = f"{GitServiceCaller.get_service_url()}/{token}"

    repo = git.Repo.init()
    print("[green]Repository has initialized[/green]")

    origin = repo.create_remote("origin", git_url)
    origin.fetch()
    repo.git.checkout("master")
    origin.pull()
    print("[green]Repository is ready.[/green]:rocket:")
    print(f":point_right: [blue]Go to project directory: cd {project_name}/[/blue]")


def clone(project_id: str) -> None:
    project = CrudServiceCaller(service_name="job", entity_name="project").get_entity_with_id(entity_id=project_id)

    initialize_git_repo(project=project)
