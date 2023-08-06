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
import io
import requests

from typing import Any
from abc import ABC, abstractmethod
from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile

from gintel.utils import Tokens

# %%
token_cache = Tokens()


# %%
class Endpoint(ABC):
    def __init__(self, name: str, token: str | None = None) -> None:
        self._init_name(name)
        self._init_token(token)

    def _init_name(self, name: str) -> None:
        if name in token_cache.services:
            self.name = name
        else:
            raise Exception(f"{name.title()} not a valid service.")

    def _init_token(self, token: str | None = None) -> None:
        if token is None:
            if self.name in token_cache.defined:
                self.token = token_cache.get(self.name)
            else:
                raise Exception(
                    f"{self.name.title()} token not passed, and not available in local cache."
                )
        else:
            self.token = token

    def _validate_token(self) -> bool:
        if not self.access:
            raise Exception("Cannot access the API, token may be invalid.")

    @abstractmethod
    def _init_endpoints(self) -> None:
        raise NotImplementedError()

    @property
    @abstractmethod
    def access(self) -> bool:
        raise NotImplementedError()


# %%
class Mapbox(Endpoint):
    def __init__(self, token: str | None = None) -> None:
        super().__init__("mapbox", token)
        self._init_endpoints()
        self._validate_token()

    def _init_endpoints(self) -> None:
        self.__base: str = "https://api.mapbox.com"
        self.__access: str = f"{self.__base}/tokens/v2?access_token={self.token}"
        self.__satellite: str = f"{self.__base}/v4/mapbox.satellite"
        self.__elevation: str = f"{self.__base}/v4/mapbox.terrain-rgb"

    def _satellite(self, tile_x: int, tile_y: int, zoom: int) -> str:
        return f"{self.__satellite}/{str(zoom)}/{str(tile_x)}/{str(tile_y)}@2x.png?access_token={self.token}"

    def _elevation(self, tile_x: int, tile_y: int, zoom: int) -> str:
        return f"{self.__elevation}/{str(zoom)}/{str(tile_x)}/{str(tile_y)}@2x.pngraw?access_token={self.token}"

    def satellite(self, tile_x: int, tile_y: int, zoom: int) -> JpegImageFile:
        resp = requests.get(self._satellite(tile_x, tile_y, zoom), stream=True)
        image = Image.open(io.BytesIO(resp.raw.data))
        return image

    def elevation(self, tile_x: int, tile_y: int, zoom: int) -> JpegImageFile:
        resp = requests.get(self._elevation(tile_x, tile_y, zoom), stream=True)
        image = Image.open(io.BytesIO(resp.raw.data))
        return image

    @property
    def access(self) -> bool:
        resp = requests.get(self.__access)
        return resp.json()["code"] == "TokenValid"


# %%
class Interface:
    def __init__(self, **kwargs):
        """
        The keywords arguments passed represent if the user wants to pass tokens directly.
        """
        self.__validate_token_kwargs(kwargs)
        self.mapbox = Mapbox(
            token=kwargs["mapbox"] if "mapbox" in kwargs.keys() else None
        )

    def __validate_token_kwargs(self, kwargs: dict[str, str]) -> None:
        invalid_services = set(kwargs.keys()).difference(token_cache.services)
        if len(invalid_services):
            raise Exception(f"Invalid service name passed: {invalid_services}")

    def query(self, **kwargs) -> Any:
        pass
