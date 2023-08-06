import sys
from typing import Optional, TypeVar

if sys.version_info < (3, 8):
    from typing_extensions import Protocol
else:
    from typing import Protocol

from .context import Context

T = TypeVar("T")


class Outputter(Protocol[T]):
    def write(self, value: T, *, context: Optional[Context[T]] = None) -> None:
        ...
