"""M2.1 backend-neutral IRC service taxonomy and multi-instance model."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Protocol

class ServiceKind(str,Enum):
    BOUNCER="bouncer"; BOT="bot"; CLIENT="client"
class ServiceState(str,Enum):
    RUNNING="running"; STOPPED="stopped"; UNAVAILABLE="unavailable"; UNKNOWN="unknown"

@dataclass(frozen=True,slots=True)
class ServiceId:
    kind:ServiceKind
    name:str
    def __post_init__(self):
        if not self.name or not self.name.replace("-","").replace("_","").isalnum():
            raise ValueError("service instance name must contain only letters, digits, '-' or '_'")

@dataclass(frozen=True,slots=True)
class ServiceInfo:
    service_id:ServiceId
    state:ServiceState
    backend:str
    autostart:bool=False
    @property
    def name(self)->str:return self.service_id.name
    @property
    def kind(self)->ServiceKind:return self.service_id.kind

class ServiceBackend(Protocol):
    service_id:ServiceId
    def status(self)->ServiceInfo: ...
    def start(self)->ServiceInfo: ...
    def stop(self)->ServiceInfo: ...
    def restart(self)->ServiceInfo: ...

class MutationDisabled(RuntimeError):pass

class PlaceholderBackend:
    def __init__(self,kind:ServiceKind,name:str,backend:str):
        self.service_id=ServiceId(kind,name);self.backend=backend
    @property
    def name(self)->str:return self.service_id.name
    def status(self)->ServiceInfo:return ServiceInfo(self.service_id,ServiceState.UNAVAILABLE,self.backend)
    def _deny(self)->ServiceInfo:raise MutationDisabled(f"{self.name}: runtime mutation backend not configured")
    start=stop=restart=_deny

class ServiceRegistry:
    def __init__(self,backends:tuple[ServiceBackend,...]|None=None):
        defaults=(
            PlaceholderBackend(ServiceKind.BOUNCER,"main","soju"),
            PlaceholderBackend(ServiceKind.BOUNCER,"znc1","znc"),
            PlaceholderBackend(ServiceKind.BOUNCER,"legacy","psybnc"),
            PlaceholderBackend(ServiceKind.BOUNCER,"muh1","muh"),
            PlaceholderBackend(ServiceKind.BOUNCER,"bip1","bip"),
            PlaceholderBackend(ServiceKind.BOUNCER,"pounce1","pounce"),
            PlaceholderBackend(ServiceKind.BOT,"eggdrop1","eggdrop"),\n            PlaceholderBackend(ServiceKind.BOT,"limnoria1","limnoria"),\n            PlaceholderBackend(ServiceKind.BOT,"sopel1","sopel"),\n            PlaceholderBackend(ServiceKind.BOT,"errbot1","errbot"),
            PlaceholderBackend(ServiceKind.CLIENT,"weechat","weechat"),
            PlaceholderBackend(ServiceKind.CLIENT,"irssi","irssi"),\n            PlaceholderBackend(ServiceKind.CLIENT,"bitchx","bitchx"),
        )
        self._items={(b.service_id.kind,b.service_id.name):b for b in (backends or defaults)}
    def get(self,name:str,kind:ServiceKind|None=None)->ServiceBackend|None:
        if kind is not None:return self._items.get((kind,name))
        matches=[b for (_,n),b in self._items.items() if n==name]
        return matches[0] if len(matches)==1 else None
    def statuses(self,kind:ServiceKind|None=None)->tuple[ServiceInfo,...]:
        return tuple(b.status() for (k,_),b in self._items.items() if kind is None or k==kind)
