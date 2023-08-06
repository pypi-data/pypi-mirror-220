from __future__ import annotations

import dataclasses


class SliceToPyDistError(Exception):
    pass


@dataclasses.dataclass
class DistPackageInfo:
    name: str
    version: str
    authors: list[str]
    summary: str
    requires_python: str
