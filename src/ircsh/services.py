"""M2 backend-neutral IRC service abstraction."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Protocol

class ServiceState(str,Enum):
    RUNNING="running"; STOPPED="stopped"; UNAVAILABLE="unavailable"; UNKNOWN="unknown"

@dataclass(frozen=True,slots=True)
class ServiceInfo:
    name:str
    state:ServiceState
    backend:str
    autostart:bool=False

class ServiceBackend(Protocol):
    name:str
    def status(self)->ServiceInfo: ...
    def start(self)->ServiceInfo: ...
    def stop(self)->ServiceInfo: ...
    def restart(self)->ServiceInfo: ...

class MutationDisabled(RuntimeError): pass

class PlaceholderBackend:
    """Safe adapter skeleton: reports state but cannot mutate the host yet."""
    def __init__(self,name:str,backend:str):
        self.name=name; self.backend=backend
    def status(self)->ServiceInfo:
        return ServiceInfo(self.name,ServiceState.UNAVAILABLE,self.backend)
    def _deny(self)->ServiceInfo:
        raise MutationDisabled(f"{self.name}: runtime mutation backend not configured")
    start=stop=restart=_deny

class ServiceRegistry:
    def __init__(self,backends:tuple[ServiceBackend,...]|None=None):
        self._items={b.name:b for b in (backends or (
            PlaceholderBackend("soju","soju"),
            PlaceholderBackend("znc","znc"),
            PlaceholderBackend("eggdrop","placeholder"),
            PlaceholderBackend("weechat","placeholder"),
            PlaceholderBackend("irssi","placeholder"),
        ))}
    def names(self)->tuple[str,...]: return tuple(self._items)
    def get(self,name:str)->ServiceBackend|None: return self._items.get(name)
    def statuses(self)->tuple[ServiceInfo,...]: return tuple(x.status() for x in self._items.values())
