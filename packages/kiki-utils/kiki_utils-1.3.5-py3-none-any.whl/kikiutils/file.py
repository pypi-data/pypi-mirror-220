import io
import magic
import os
import shutil

from typing import Callable, Literal, overload

from .decorators import try_and_get_bool, try_and_get_data
from .typehint import P, PathOrStr, T


# File

def clear_dir(path: PathOrStr):
    """Clear dir (Remove and create)."""

    return rmdir(path) and mkdirs(path)


@try_and_get_bool
def del_file(path: PathOrStr):
    """Del file."""

    os.remove(path)


def get_file_mime(file: bytes | io.BytesIO | io.FileIO):
    """Get file mime."""

    is_file = getattr(file, 'read', None) != None
    data = file.read(2048) if is_file else file[:2048]
    file_mime = magic.from_buffer(data, mime=True)

    if is_file:
        file.seek(0)

    return file_mime.split('/')


@try_and_get_data
def get_file_size(path: PathOrStr):
    return os.stat(path).st_size


@try_and_get_bool
def mkdir(path: PathOrStr):
    """Create dir."""

    os.mkdir(path)


@try_and_get_bool
def mkdirs(path: PathOrStr):
    """Create dir (use makedirs)."""

    os.makedirs(path, exist_ok=True)


@try_and_get_bool
def move_file(path: PathOrStr, target_path: PathOrStr):
    """Move file or dir."""

    shutil.move(path, target_path)


@try_and_get_data
def read_file(path: PathOrStr):
    """Read file."""

    with open(path, 'rb') as f:
        return f.read()


@try_and_get_bool
def rename(path: PathOrStr, name: PathOrStr):
    """Rename file or dir."""

    os.rename(path, name)


@try_and_get_bool
def rmdir(path: PathOrStr):
    """Remove dir."""

    shutil.rmtree(path)


@try_and_get_data
def save_file(path: PathOrStr, file: bytes | io.BytesIO | io.FileIO | str, replace: bool = True):
    """Save file."""

    mode = 'w' if isinstance(file, str) else 'wb'

    if os.path.exists(path) and not replace:
        raise FileExistsError()
    if getattr(file, 'read', None):
        file = file.read()
    with open(path, mode) as f:
        return f.write(file)


@overload
def save_file_as_bytesio(save_fnc: Callable[P, T], get_bytes: Literal[True], **kwargs) -> bytes: ...
@overload
def save_file_as_bytesio(save_fnc: Callable[P, T], get_bytes: Literal[False], **kwargs) -> io.BytesIO: ...
@overload
def save_file_as_bytesio(save_fnc: Callable[P, T]) -> io.BytesIO: ...
def save_file_as_bytesio(save_fnc: Callable[P, T], get_bytes: bool = False, **kwargs):
    """Save file to io.BytesIO."""

    with io.BytesIO() as output:
        save_fnc(output, **kwargs)
        file_bytes = output.getvalue()

    if get_bytes:
        return file_bytes

    return io.BytesIO(file_bytes)
