# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: base
#     language: python
#     name: python3
# ---

# %%
import os

from pyeio import easy
from typing import Any
from pathlib import Path
from rich.console import Console

from gintel.env import FILES
from gintel.env import TOKENS


# %%
def make_package_directory():
    if not Path(FILES).exists():
        Path(FILES).mkdir()


# %%
class Tokens:
    def __init__(self) -> None:
        self.data = easy.load(TOKENS)

    @property
    def services(self) -> list[str]:
        return list(self.data.keys())

    @property
    def defined(self) -> list[str]:
        return [k for k, v in self.data.items() if v is not None]

    @property
    def undefined(self) -> list[str]:
        return [k for k, v in self.data.items() if v is None]

    def save(self) -> None:
        easy.save(self.data, TOKENS)

    def get(self, name: str) -> str:
        if name in self.data.keys():
            return self.data[name]
        else:
            raise Exception("Invalid Token Name")

    def update(self, name: str, token: str) -> None:
        if name in self.data.keys():
            self.data[name] = token
            self.save()
        else:
            raise Exception("Invalid Token Name")

    def remove(self, name: str) -> bool:
        if name in self.data.keys():
            self.data[name] = None
            self.save()
        else:
            raise Exception("Invalid Token Name")


# %%
tokens = Tokens()

# %%


def vprint(x: Any, verbose: bool = True) -> None:
    if verbose:
        Console().print(x)


def clear():
    os.system("cls" if os.name == "nt" else "clear")
