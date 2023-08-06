from __future__ import annotations
from typing import List, Optional
from landingzone_organization import Account as LandingZoneAccount
from aws_network_firewall.cidr_ranges import CidrRanges
from aws_network_firewall.rule import Rule


class Account(LandingZoneAccount):
    __rules: List[Rule]
    __cidr_ranges: CidrRanges

    def __init__(
        self, name: str, account_id: str, cidr_ranges: CidrRanges, rules: List[Rule]
    ) -> None:
        super().__init__(name, account_id)
        self.__cidr_ranges = cidr_ranges
        self.__rules = list(map(self.__enrich_rule, rules))

    def __enrich_rule(self, rule: Rule) -> Rule:
        list(
            map(
                lambda source: source.resolve_region_cidr_ranges(self.__cidr_ranges),
                rule.sources,
            )
        )
        list(
            map(
                lambda destination: destination.resolve_region_cidr_ranges(
                    self.__cidr_ranges
                ),
                rule.destinations,
            )
        )

        return rule

    @property
    def rules(self) -> List[Rule]:
        return self.__rules
