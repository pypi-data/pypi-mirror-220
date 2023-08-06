from pathlib import Path
from typing import ParamSpec, TypeVar


__all__ = [
    'P',
    'PathOrStr',
    'T'
]

BytesOrStr = bytes | str
P = ParamSpec('P')
PathOrStr = Path | str
T = TypeVar('T')
