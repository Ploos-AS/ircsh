"""Concrete IRC service adapters."""
from __future__ import annotations
from .runtime import Runtime,RuntimeState
from .services import ServiceId,ServiceInfo,ServiceKind,ServiceState

class SojuBackend:
    """Soju adapter using a narrow runtime API; no shell command construction."""
    backend="soju"
    def __init__(self,name:str,runtime:Runtime,unit:str="soju.service"):
        self.service_id=ServiceId(ServiceKind.BOUNCER,name)
        self.runtime=runtime
        if unit!="soju.service":raise ValueError("unsupported soju runtime unit")
        self.unit=unit
    def status(self)->ServiceInfo:
        state={RuntimeState.ACTIVE:ServiceState.RUNNING,RuntimeState.INACTIVE:ServiceState.STOPPED,
               RuntimeState.MISSING:ServiceState.UNAVAILABLE}.get(self.runtime.state(self.unit),ServiceState.UNKNOWN)
        return ServiceInfo(self.service_id,state,self.backend)
    def start(self)->ServiceInfo:self.runtime.start(self.unit);return self.status()
    def stop(self)->ServiceInfo:self.runtime.stop(self.unit);return self.status()
    def restart(self)->ServiceInfo:self.runtime.restart(self.unit);return self.status()

class ZncBackend:
    """ZNC adapter using the same narrow runtime boundary as soju."""
    backend="znc"
    def __init__(self,name:str,runtime:Runtime,unit:str="znc.service"):
        self.service_id=ServiceId(ServiceKind.BOUNCER,name)
        self.runtime=runtime
        if unit!="znc.service":raise ValueError("unsupported ZNC runtime unit")
        self.unit=unit
    def status(self)->ServiceInfo:
        state={RuntimeState.ACTIVE:ServiceState.RUNNING,RuntimeState.INACTIVE:ServiceState.STOPPED,
               RuntimeState.MISSING:ServiceState.UNAVAILABLE}.get(self.runtime.state(self.unit),ServiceState.UNKNOWN)
        return ServiceInfo(self.service_id,state,self.backend)
    def start(self)->ServiceInfo:self.runtime.start(self.unit);return self.status()
    def stop(self)->ServiceInfo:self.runtime.stop(self.unit);return self.status()
    def restart(self)->ServiceInfo:self.runtime.restart(self.unit);return self.status()
