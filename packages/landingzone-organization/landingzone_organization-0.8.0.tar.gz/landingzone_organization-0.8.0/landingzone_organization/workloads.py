from __future__ import annotations

import glob
import os
from typing import List, Optional, Set, Callable

from landingzone_organization.account import Account
from landingzone_organization.schemas import safe_load_file, WorkloadSchema
from landingzone_organization.workload import Workload
from landingzone_organization.filtering import resolve_workload_name


class Workloads:
    def __init__(self, workloads: List[Workload]) -> None:
        self.__index = 0
        self.__workloads = workloads

    def __len__(self) -> int:
        return len(self.__workloads)

    def __iter__(self):
        for workload in self.__workloads:
            yield workload

    @property
    def names(self) -> Set[str]:
        return set(map(lambda workload: workload.name, self.__workloads))

    @property
    def accounts(self) -> List[Account]:
        accounts = []

        for workload in self.__workloads:
            accounts.extend(workload.accounts)

        return accounts

    @property
    def environments(self) -> Set[str]:
        environments = set()

        for workload in self.__workloads:
            environments.update(workload.environments)

        return environments

    def resolve_account(self, account: Account) -> None:
        workload_name = resolve_workload_name(account.name)

        if workload_name:
            workload = self.by_name(workload_name)

            if not workload:
                self.__workloads.append(
                    Workload(name=workload_name, display_name=None, accounts=[account])
                )
            else:
                workload.append(account)

    def by_name(self, name: str) -> Optional[Workload]:
        return next(filter(lambda w: w.name == name, self.__workloads), None)  # type: ignore

    @staticmethod
    def __load_workload_by_file(
        environment_resolver: Callable[[str], Account], path: str
    ) -> Optional[Workload]:
        data = safe_load_file(WorkloadSchema, path)

        def convert_environments_to_file_locations(environment: str) -> str:
            return os.path.join(os.path.dirname(path), f"{environment}.yaml")

        accounts_files = list(
            map(convert_environments_to_file_locations, data.get("Environments", []))
        )
        response = list(map(environment_resolver, accounts_files))
        accounts = list(filter(None, response))

        return Workload.from_dict(data, accounts)

    @classmethod
    def load_by_path(
        cls, path: str, environment_resolver: Callable[[str], Account]
    ) -> Workloads:
        def load_workload(workload_path: str) -> Optional[Workload]:
            return cls.__load_workload_by_file(
                environment_resolver=environment_resolver, path=workload_path
            )

        workloads = glob.glob(os.path.join(path, "**", "info.yaml"), recursive=True)
        response = list(map(load_workload, workloads))

        return Workloads(workloads=list(filter(None, response)))
