"""Read-only M1 provider interfaces and safe default implementations."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class Status:
    session:str="active"
    runtime:str="not configured"

class StatusProvider:
    def read(self)->Status: return Status()

class QuotaProvider:
    def read(self)->str: return "Quota backend: not configured (M1)"

class ServiceProvider:
    SERVICES=("soju","znc","eggdrop","weechat","irssi")
    def read(self)->tuple[str,...]: return self.SERVICES
