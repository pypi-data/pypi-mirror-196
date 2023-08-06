import click
import subprocess

from pick import pick
from gintel.utils import Tokens, vprint

token_cache = Tokens()


@click.group()
def entry():
    pass


@entry.group()
def cache():
    pass


@cache.command()
def explore():
    "Opens finder window at data cache location."
    pass


@cache.command()
def clear():
    "Clears cached data."
    pass


@entry.group()
def tokens():
    pass


@tokens.command()
def view():
    if len(token_cache.defined) == 0:
        vprint("[yellow]No Defined Tokens[/yellow]")
    else:
        selection = pick(options=token_cache.defined, title="Select Token")
        vprint(f"{selection[0].title()} API Token")
        vprint(f"[blue]{token_cache.get(selection[0])}[/blue]")


@tokens.command()
def add():
    if len(token_cache.undefined) == 0:
        vprint("[yellow]No Undefined Tokens[/yellow]")
    else:
        selection = pick(options=token_cache.undefined, title="Select Token")
        vprint(f"{selection[0].title()} API Token")
        api_token = str(input("❯ "))
        token_cache.update(selection[0], api_token)
        vprint(f"[green]{selection[0].title()} Token Saved[/green]")


@tokens.command()
def delete():
    if len(token_cache.defined) == 0:
        vprint("[yellow]No Defined Tokens[/yellow]")
    else:
        selection = pick(options=token_cache.defined, title="Select Token")
        token_cache.remove(selection[0])
        vprint(f"[green]{selection[0].title()} Token Deleted[/green]")


@tokens.command()
def change():
    if len(token_cache.defined) == 0:
        vprint("[yellow]No Defined Tokens[/yellow]")
    else:
        selection = pick(options=token_cache.defined, title="Select Token")
        vprint(f"New {selection[0].title()} API Token")
        api_token = str(input("❯ "))
        token_cache.update(selection[0], api_token)
        vprint(f"[green]{selection[0].title()} Token Saved[/green]")


@tokens.command()
def copy():
    if len(token_cache.defined) == 0:
        vprint("[yellow]No Defined Tokens[/yellow]")
    else:
        selection = pick(options=token_cache.defined, title="Select Token")
        api_token = token_cache.get(selection[0])
        subprocess.run("pbcopy", text=True, input=api_token)
        vprint(f"[green]{selection[0].title()} Token Copied[/green]")
