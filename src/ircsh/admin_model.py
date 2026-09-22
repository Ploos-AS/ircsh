"""Trusted administrative account-plan model."""
from __future__ import annotations
from dataclasses import dataclass
import re
from .isolation import ResourceLimits
from .model import KNOWN_CAPABILITIES
_PLAN=re.compile(r"^[a-z][a-z0-9_-]{0,31}$")
@dataclass(frozen=True,slots=True)
class AccountPlan:
 name:str
 capabilities:frozenset[str]
 limits:ResourceLimits
 def __post_init__(self):
  if not _PLAN.fullmatch(self.name):raise ValueError("invalid plan name")
  if type(self.capabilities) is not frozenset:raise TypeError("capabilities must be frozenset")
  if any(type(c) is not str or c not in KNOWN_CAPABILITIES for c in self.capabilities):raise ValueError("unknown capability")
IRC_BASIC=AccountPlan("irc-basic",frozenset({"status.read","services.read","quota.read","bouncers.read"}),ResourceLimits(services=2))
IRC_ADVANCED=AccountPlan("irc-advanced",frozenset({"status.read","services.read","quota.read","bouncers.read","bouncers.manage","bots.read","bots.manage","clients.read","clients.manage","sessions.read","sessions.manage","config.read","config.manage","logs.read"}),ResourceLimits(memory_mb=512,disk_mb=2048,connections=64,services=8))
PLANS={p.name:p for p in (IRC_BASIC,IRC_ADVANCED)}
def get_plan(name:str)->AccountPlan:
 if type(name) is not str or name not in PLANS:raise ValueError("unknown account plan")
 return PLANS[name]
