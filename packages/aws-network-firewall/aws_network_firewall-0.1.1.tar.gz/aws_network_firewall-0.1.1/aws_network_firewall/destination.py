from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from aws_network_firewall.cidr_ranges import CidrRanges


@dataclass
class Destination:
    """
    Understands a destination
    """

    description: str
    protocol: str
    port: int
    endpoint: Optional[str]
    region: Optional[str]
    cidr: Optional[str]

    def resolve_region_cidr_ranges(self, ranges: CidrRanges) -> None:
        if self.region and not self.cidr:
            cidr = ranges.by_region(self.region)
            self.cidr = cidr.value if cidr else None
