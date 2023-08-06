import sys
from typing import TypeVar

if sys.version_info < (3, 8):
    from typing_extensions import Protocol
else:
    from typing import Protocol

T = TypeVar("T", contravariant=True)
S = TypeVar("S", covariant=True)


class Deserializer(Protocol[T, S]):
    def deserialize(self, value: T) -> S:
        ...
