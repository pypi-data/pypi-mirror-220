from __future__ import annotations

from dataclasses import dataclass
from typing import Union


@dataclass
class Option:
    """
    Understands how to define options for a suricata rule
    """

    name: str
    value: Union[str, int, None] = None

    def __str__(self):
        return self.name if not self.value else f'{self.name}:"{self.value}"'
