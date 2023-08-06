import git
from rich import print

def is_git_repo():
    try:
        _ = git.Repo()
    except git.exc.InvalidGitRepositoryError:
        return False
    else:
        return True


def pull() -> None:
    if not is_git_repo():
        print("[bold red]Repository is not exist in current directory![/bold red]")
        return

    repo = git.Repo()
    origin = repo.remotes.origin

    origin.pull()
    print("[green]Repository is up to date.[/green]:rocket:")
