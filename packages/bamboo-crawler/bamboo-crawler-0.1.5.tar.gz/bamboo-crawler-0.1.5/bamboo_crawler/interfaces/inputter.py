import sys
from typing import TypeVar

if sys.version_info < (3, 8):
    from typing_extensions import Protocol
else:
    from typing import Protocol

from .context import Context

T = TypeVar("T")


class Inputter(Protocol[T]):
    def read(self) -> Context[T]:
        ...

    def done(self) -> None:
        ...
