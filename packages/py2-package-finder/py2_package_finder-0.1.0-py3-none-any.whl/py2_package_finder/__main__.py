import datetime
from importlib.metadata import PackageNotFoundError, version
from json import JSONDecodeError
from typing import Optional

import requests
import typer
from rich import print
from rich.progress import track

app = typer.Typer()


try:
    __version__ = version("py2-package-finder")
except PackageNotFoundError:
    __version__ = "dev"


def version_callback(value: bool):
    if value:
        print(__version__)
        raise typer.Exit()


def success(msg):
    print(f"[green]{msg}[/green]")


def error(msg):
    print(f"[red]{msg}[/red]")


def get_package_versions(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"

    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
    except (requests.HTTPError, requests.ConnectionError, JSONDecodeError) as exc:
        error(f"Error: {str(exc)}")
        raise typer.Exit(1)
    return {
        package_version: {"upload_time_iso_8601": release[0]["upload_time_iso_8601"]}
        for package_version, release in data["releases"].items()
        if release
    }


def get_python_for_version(package_name, package_version, python_version):
    url = f"https://pypi.org/pypi/{package_name}/{package_version}/json"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
    except (requests.HTTPError, requests.ConnectionError, JSONDecodeError) as exc:
        error(f"Error: {str(exc)}")
        raise typer.Exit(1)
    classifiers = data["info"]["classifiers"]
    for classifier in classifiers:
        if f"Python :: {python_version}" in classifier:
            return True
    return False


@app.command()
def main(
    package_name: str,
    python_version: Optional[str] = typer.Option("2.7", "--python"),
    _: Optional[bool] = typer.Option(None, "-v", "--version", callback=version_callback, is_eager=True),
):
    versions = get_package_versions(package_name)
    latest_version = None
    latest_version_upload_time_iso_8601 = datetime.datetime(2000, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)
    for package_version, release in track(versions.items(), description="Searching all released versions..."):
        if get_python_for_version(package_name, package_version, python_version):
            upload_time = datetime.datetime.fromisoformat(release["upload_time_iso_8601"].replace("Z", "+00:00"))
            if upload_time > latest_version_upload_time_iso_8601:
                latest_version_upload_time_iso_8601 = upload_time
                latest_version = package_version
    if latest_version:
        success(f"[bold]{latest_version}[/bold] released @ {latest_version_upload_time_iso_8601}")
    else:
        error(f"Can't find any version that has a classification for {python_version}")


if __name__ == "__main__":
    app()
