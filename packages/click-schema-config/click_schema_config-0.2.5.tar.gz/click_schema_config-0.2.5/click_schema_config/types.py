from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed import StrPath
from typing import Any, TypeAlias, Iterable

from dataclasses import dataclass


@dataclass
class Variable:
    option_name: str
    programmatic_name: str
    type: str | None = None
    value: Any | None = None
    description: str | None = None
    required: bool = False


Section: TypeAlias = dict[str, Variable]
Config: TypeAlias = dict[str | None, Section]

FileLike: TypeAlias = "StrPath | Iterable[str]"
