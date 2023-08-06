from orjson import dumps as odumps, loads as oloads

from .aiofile import aread_file, asave_file
from .file import read_file, save_file
from .string import camel_to_snake, snake_to_camel
from .typehint import PathOrStr


# Dict

def dict_key_camel_to_snake(data: dict[str]):
    return {camel_to_snake(k): v for k, v in data.items()}


def dict_key_snake_to_camel(data: dict[str]):
    return {snake_to_camel(k): v for k, v in data.items()}


# Json operate

async def aread_json(path: PathOrStr):
    """Async read json file with orjson."""

    return oloads(await aread_file(path))


async def asave_json(path: PathOrStr, data: dict | list):
    """Async save json file with orjson."""

    return await asave_file(path, odumps(data))


def read_json(path: PathOrStr):
    """Read json file with orjson."""

    return oloads(read_file(path))


def save_json(path: PathOrStr, data: dict | list):
    """Save json file with orjson."""

    return save_file(path, odumps(data))
