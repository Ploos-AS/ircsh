"""M1 account and capability model."""
from __future__ import annotations
from dataclasses import dataclass

KNOWN_CAPABILITIES=frozenset({"status.read","quota.read","services.read","bots.read","bots.manage","bouncers.read","bouncers.manage"})

@dataclass(frozen=True,slots=True)
class Account:
    name:str
    capabilities:frozenset[str]

    def allows(self, capability:str)->bool:
        return capability in self.capabilities
