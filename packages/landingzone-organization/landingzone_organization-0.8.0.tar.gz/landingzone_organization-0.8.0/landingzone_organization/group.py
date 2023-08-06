from __future__ import annotations
from typing import List, Optional, Union
from dataclasses import dataclass, field

from landingzone_organization.organization_unit import OrganizationUnit
from landingzone_organization.organization import Organization
from landingzone_organization.account import Account


@dataclass
class Group:
    """
    Understands grouping of AWS Accounts within the landing zone
    """

    name: str
    default_region: str
    organizational_unit: List[str] = field(default_factory=list)
    _organization: Optional[Organization] = None

    @property
    def accounts(self) -> List[Account]:
        if not self._organization:
            return []

        champion: Union[Organization, OrganizationUnit] = self._organization

        for ou in self.organizational_unit:
            challenger = champion.by_name(ou)

            if challenger:
                champion = challenger

        return champion.accounts  # type: ignore

    def organization(self, organization: Organization) -> None:
        self._organization = organization
