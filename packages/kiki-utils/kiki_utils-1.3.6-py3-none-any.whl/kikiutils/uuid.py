from uuid import uuid1

from .aiofile import aread_file, asave_file
from .file import read_file, save_file
from .typehint import PathOrStr


# UUID

async def aget_uuid(save_path: PathOrStr = './uuid.uuid'):
    if now_uuid := await aread_file(save_path):
        return now_uuid.decode()

    now_uuid = str(uuid1())
    await asave_file(save_path, now_uuid)
    return now_uuid


def get_uuid(save_path: PathOrStr = './uuid.uuid'):
    if now_uuid := read_file(save_path):
        return now_uuid.decode()

    now_uuid = str(uuid1())
    save_file(save_path, now_uuid)
    return now_uuid
