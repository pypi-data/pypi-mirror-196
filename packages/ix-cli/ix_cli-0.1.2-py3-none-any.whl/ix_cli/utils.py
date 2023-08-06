import os
import re
import sys
import json
import rich
import requests
from pathlib import Path
from rich.console import Console
from rich.progress import (
    Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
    )
from copy import deepcopy
from typing import Union

__all__ = [
    "uploadFromFile",
    "uploadFromStdin",
    "download",
    "initHistory",
    "HISTORY_PATH",
    "resetHistory",
    "PROVIDER_URL",
    "console",
    "sanitize",
    ]

Pbar = Progress(
    SpinnerColumn(),
    "●",
    TextColumn("[bold cyan]Sanitizing data[/bold cyan] [bold magenta](Windows only)[/bold magenta]", justify="right"),
    "●",
    TimeElapsedColumn(),
)

console = Console()

PROVIDER_URL = "http://ix.io"

HISTORY_PATH = Path().home() / ".ix" / "history.json"

def initHistory(silent: bool = True):
    try:
        HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not HISTORY_PATH.exists():
            HISTORY_PATH.write_text("[]")
    except OSError:
        if not silent:
            console.print(f"Could not create history file at {HISTORY_PATH}", style="bold red")

def resetHistory():
    HISTORY_PATH.unlink()
    initHistory()

def updateHistory(response, src: Union[Path,str], nlines: int = 100):
    if not HISTORY_PATH.exists():
        return
    jhistory = json.loads(HISTORY_PATH.read_text())
    jhistory.append({
        "url": response.text,
        "id": response.text.split("/")[-1],
        "name": src.name if isinstance(src, Path) else src[:min(15, src.find(" "))],
        })
    if len(jhistory) > nlines:
        jhistory = jhistory[-nlines:]
    HISTORY_PATH.write_text(json.dumps(jhistory, indent=4))

def uploadFromFile(filepath: Path) -> str:
    """Uploads a file to ix.io and returns the URL."""
    files = {"f:1": open(filepath, "rb")}
    response = requests.post(PROVIDER_URL, files=files)
    if response.status_code == 200:
        updateHistory(response, filepath.name)
    return response.text

def pipeInput() -> str:
    """Returns the piped input if any."""
    return "".join(sys.argv[1:]).replace("s", "") if sys.stdin.isatty() else sys.stdin.buffer.read().decode("utf-8")

def uploadFromStdin(param: str = None) -> str:
    """Uploads stdin to ix.io and returns the URL."""
    data = param or pipeInput()
    sys.stdin.close()
    if '{' in data and sys.platform == 'win32':
        with Pbar as pbar:
            task = pbar.add_task("Data Sanitization", total=1)
            data = sanitize(data)
            pbar.update(task, description="[bold green]Done[/bold green]", completed=True)
        
    if not data:
        console.print("[bold red]No data found in stdin.[/bold red]")
        console.print("[bold yellow]Usage:[/bold yellow]")
        console.print(" -  ix s <data>")
        console.print(" -  echo <data> | ix s")
        console.print(" -  cat <file>  | ix s")
        return
    response = requests.post(PROVIDER_URL, data={"f:1": data})
    if response.status_code == 200:
        updateHistory(response, f"stdin:{data[:5]}")
    return response.text

def download(url: str) -> str:
    """Downloads a file from ix.io and returns the contents."""
    url = url.strip()
    response = requests.get(url)
    return response.text

def winIterKeys(subparam: str):
    for item in subparam.split(","):
        key, value = item.split(":")
        key = key.lstrip()
        if '[' in value:
            for lv in value[1:-1].split("@lsep@"):
                new_value = value.replace(lv, f'"{lv}"')
        else:
            new_value = value
        kvstr = f'"{key}":"{new_value}"'
        subparam = subparam.replace(item, kvstr)
    return subparam

def subDictFix(subparam: str):
    
    nextdict = subparam.find("{")
    subparam = subparam[:nextdict]
    return winIterKeys(subparam)

def sanitize(param: str):
    try:
        return windowsDictRepair(param)
    except Exception as e:
        return param

def windowsDictRepair(param: str):
    if not param:
        return param
    chars = ['{', '}', ":"]
    if any(x not in param for x in chars):
        return param
    param = param[1:-1]
    for listvar in re.findall(r'\[(.*)\]', param):
        param = param.replace(listvar, listvar.replace(",", "@lsep@"))

    non_nested = deepcopy(param)
    for dictvar in re.findall(r'\{(.*)\}', param):
        param = param.replace(dictvar, subDictFix(dictvar))
        non_nested = non_nested.replace(dictvar, '')
    non_nested = non_nested.replace("{", "").replace("}", "")
    param = param.replace(non_nested, winIterKeys(non_nested))
    param = param.replace(':""', ':')
    param = param.replace("@lsep@", ",")
    return '{' + param + '}'
