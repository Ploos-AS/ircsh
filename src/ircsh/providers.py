"""Read-only status/quota providers and M2 service provider."""
from __future__ import annotations
from dataclasses import dataclass
from .services import ServiceInfo,ServiceKind,ServiceRegistry

@dataclass(frozen=True,slots=True)
class Status:
    session:str="active"
    runtime:str="not configured"

class StatusProvider:
    def read(self)->Status: return Status()

class QuotaProvider:
    def read(self)->str: return "Quota backend: not configured (M1)"

class ServiceProvider:
    def __init__(self,registry:ServiceRegistry|None=None):
        self.registry=registry or ServiceRegistry()
    def read(self)->tuple[ServiceInfo,...]:
        return self.registry.statuses()
    def bots(self)->tuple[ServiceInfo,...]: return self.registry.statuses(ServiceKind.BOT)
    def bot(self,name:str): return self.registry.get(name,ServiceKind.BOT)
