import typer
import rich
import json
import sys
import re

from pathlib import Path
from rich.table import Table

from .utils import (
    uploadFromFile,
    uploadFromStdin,
    download,
    initHistory,
    resetHistory,
    console,
    windowsDictRepair,
    HISTORY_PATH,
    PROVIDER_URL
)

PROVIDER_NAME = PROVIDER_URL.split("//")[-1]

app = typer.Typer(
    name="ix",
    help=f"A CLI for interacting with the {PROVIDER_NAME} pastebin service.",
    no_args_is_help=True,
    rich_help_panel="rich",
    rich_markup_mode="rich",
)

@app.command(
    "f",
    help=f"Upload a file to {PROVIDER_NAME}",
    no_args_is_help=True,
)
def from_file(
    filepath: Path = typer.Argument(
        ...,
        help="The path to the file to upload.", 
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True
        ),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode.")
    ):
    initHistory(silent = not debug)
    console.print(uploadFromFile(filepath))
    
@app.command(
    "s",
    help=f"Upload stdin to {PROVIDER_NAME}",
    no_args_is_help=False,
)
def from_stdin(
    param: str = typer.Argument(None, help=f"sdtin input to upload to {PROVIDER_NAME}, defaults to sys.argv"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode."),
):
    param = ' '.join(sys.argv[2:])
    param = param if param.strip() else None
    initHistory(silent = not debug)
    if response := uploadFromStdin(param):
        console.print(response)
    
@app.command("h", help="Show the history of uploaded files.")
def history():
    if not HISTORY_PATH.exists():
        console.print("No history found.", style="bold red")
        return
    jhistory = json.loads(HISTORY_PATH.read_text())
    table = Table(show_header=True, header_style="bold magenta")
    
    table.add_column("ID", style="bold red", width=12)
    table.add_column("Content-Start", style="bold yellow", justify="center")
    table.add_column("Url", style="bold cyan", justify="center")
    
    for x in jhistory:
        table.add_row(x["id"], x["name"], x["url"])
        
    console.print(table)
    
    
@app.command(
    "g",
    help=f"Download a file from {PROVIDER_NAME}",
    no_args_is_help=True,
)
def get(
    param: str = typer.Argument(
        ...,
        help="The URL/ID/Name of the file to download.",
    ),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode."),
    ):
    initHistory(silent = not debug)
    if param.startswith("http"):
        url = param
    elif re.match(r"^[a-zA-Z0-9]+$", param):
        url = f"http://{PROVIDER_NAME}/{param}"
    else:
        jhistory = json.loads(history.read_text())
        url = next((x["url"] for x in jhistory if x["id"] == param or x["name"] == param), None)
        if not url:
            console.print(f"Could not find {param} in history", style="bold red")
            return
        
    console.print(download(url))
    
@app.command("rmh", help="Clear the history of uploaded files.")
def rm_history():
    resetHistory()
    console.print("History cleared.", style="bold green")

@app.command("x", help="Export the history of uploaded files.")
def export_history(
    nlines: int = typer.Option(None, "--num-lines", "-n", help="Number of past lines to export."),
    ):
    if not HISTORY_PATH.exists():
        console.print("No history found.", style="bold red")
        return
    jhistory = json.loads(HISTORY_PATH.read_text())
    export = jhistory[-nlines:] if nlines else jhistory
    console.print(json.dumps(windowsDictRepair(jhistory), indent=4))

@app.command("xl", help="Export last line of the history of uploaded files.")
def export_last_history():
    if not HISTORY_PATH.exists():
        console.print("No history found.", style="bold red")
        return
    jhistory = json.loads(HISTORY_PATH.read_text())
    console.print(json.dumps(windowsDictRepair(jhistory[-1]), indent=4))

    
############################################
##### Aliases for the commands above #######
############################################

@app.command("file", hidden=True)
def file_alias(
    filepath: Path = typer.Argument(
        ...,
        help="The path to the file to upload.", 
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True
        ),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode.")
):
    from_file(filepath, debug)

@app.command("stdin", hidden=True)
def stdin_alias(
    param: str = typer.Argument(None, help=f"sdtin input to upload to {PROVIDER_NAME}, defaults to sys.argv"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode."),
):
    from_stdin(param, debug)

@app.command("hist", hidden=True)
def hist_alias():
    history()

@app.command("get", hidden=True)
def get_alias(
    param: str = typer.Argument(
        ...,
        help="The URL/ID/Name of the file to download.",
    ),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode."),
):
    get(param, debug)