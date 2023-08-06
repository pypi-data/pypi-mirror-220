import aioshutil
import io

from aiofiles import open as aopen, os as aos

from .decorators import try_and_get_bool, try_and_get_data
from .typehint import PathOrStr


# Async File

async def aclear_dir(path: PathOrStr):
    """Async clear dir (Remove and create)."""

    return await armdir(path) and await amkdirs(path)


@try_and_get_bool
async def adel_file(path: PathOrStr):
    """Async del file."""

    await aos.remove(path)


@try_and_get_data
async def aget_file_size(path: PathOrStr):
    """Async get file size."""

    return (await aos.stat(path)).st_size


@try_and_get_bool
async def amkdir(path: PathOrStr):
    """Async create dir."""

    await aos.mkdir(path)


@try_and_get_bool
async def amkdirs(path: PathOrStr):
    """Async create dir (use makedirs)."""

    await aos.makedirs(path, exist_ok=True)


@try_and_get_bool
async def amove_file(path: PathOrStr, target_path: PathOrStr):
    """Move file or dir."""

    await aioshutil.move(path, target_path)


@try_and_get_data
async def aread_file(path: PathOrStr, **kwargs):
    """Async read file."""

    async with aopen(path, 'rb', **kwargs) as f:
        return await f.read()


@try_and_get_bool
async def arename(path: PathOrStr, name: PathOrStr):
    """Async rename file or dir."""

    await aos.rename(path, name)


@try_and_get_bool
async def armdir(path: PathOrStr):
    """Async Remove dir."""

    await aioshutil.rmtree(path)


@try_and_get_data
async def asave_file(path: PathOrStr, file: bytes | io.BytesIO | io.FileIO | str, replace: bool = True, **kwargs):
    """Async save file."""

    mode = 'w' if isinstance(file, str) else 'wb'

    if await aos.path.exists(path) and not replace:
        raise FileExistsError()
    if getattr(file, 'read', None):
        file = file.read()
    async with aopen(path, mode, **kwargs) as f:
        return await f.write(file)
