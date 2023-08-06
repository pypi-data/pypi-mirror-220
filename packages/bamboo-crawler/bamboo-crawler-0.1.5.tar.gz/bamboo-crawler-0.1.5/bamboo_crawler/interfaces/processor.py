from __future__ import annotations

import sys
from typing import Any, Iterable, TypeVar

if sys.version_info < (3, 8):
    from typing_extensions import Protocol
else:
    from typing import Protocol

from .context import Context

T = TypeVar("T", contravariant=True)
S = TypeVar("S", covariant=True)


class Processor(Protocol[T, S]):
    def process(
        self, value: T, *, context: Context[Any] | None = None
    ) -> Iterable[S]:
        ...
