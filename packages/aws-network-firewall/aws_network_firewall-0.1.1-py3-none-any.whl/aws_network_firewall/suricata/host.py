from __future__ import annotations

from dataclasses import dataclass
from typing import Union


@dataclass
class Host:
    """
    Understands a source and/or destination defenition
    """

    address: str = "any"
    port: Union[str, int] = "any"

    def __str__(self):
        return f"{self.address} {self.port}"
