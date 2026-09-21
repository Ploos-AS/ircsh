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

class PsybncBackend:
    """psyBNC adapter. Lifecycle is allowed only through its dedicated isolated unit."""
    backend="psybnc"
    def __init__(self,name:str,runtime:Runtime,unit:str="ircsh-psybnc.service"):
        self.service_id=ServiceId(ServiceKind.BOUNCER,name)
        self.runtime=runtime
        if unit!="ircsh-psybnc.service":raise ValueError("unsupported psyBNC runtime unit")
        self.unit=unit
    def status(self)->ServiceInfo:
        state={RuntimeState.ACTIVE:ServiceState.RUNNING,RuntimeState.INACTIVE:ServiceState.STOPPED,
               RuntimeState.MISSING:ServiceState.UNAVAILABLE}.get(self.runtime.state(self.unit),ServiceState.UNKNOWN)
        return ServiceInfo(self.service_id,state,self.backend)
    def start(self)->ServiceInfo:self.runtime.start(self.unit);return self.status()
    def stop(self)->ServiceInfo:self.runtime.stop(self.unit);return self.status()
    def restart(self)->ServiceInfo:self.runtime.restart(self.unit);return self.status()

class MuhBackend:
    """muh legacy bouncer adapter, pinned to an isolated runtime target."""
    backend="muh"
    def __init__(self,name:str,runtime:Runtime,unit:str="ircsh-muh.service"):
        self.service_id=ServiceId(ServiceKind.BOUNCER,name);self.runtime=runtime
        if unit!="ircsh-muh.service":raise ValueError("unsupported muh runtime unit")
        self.unit=unit
    def status(self)->ServiceInfo:
        state={RuntimeState.ACTIVE:ServiceState.RUNNING,RuntimeState.INACTIVE:ServiceState.STOPPED,
               RuntimeState.MISSING:ServiceState.UNAVAILABLE}.get(self.runtime.state(self.unit),ServiceState.UNKNOWN)
        return ServiceInfo(self.service_id,state,self.backend)
    def start(self)->ServiceInfo:self.runtime.start(self.unit);return self.status()
    def stop(self)->ServiceInfo:self.runtime.stop(self.unit);return self.status()
    def restart(self)->ServiceInfo:self.runtime.restart(self.unit);return self.status()

class BipBackend:
    """BIP bouncer adapter using a dedicated controlled runtime target."""
    backend="bip"
    def __init__(self,name:str,runtime:Runtime,unit:str="ircsh-bip.service"):
        self.service_id=ServiceId(ServiceKind.BOUNCER,name);self.runtime=runtime
        if unit!="ircsh-bip.service":raise ValueError("unsupported BIP runtime unit")
        self.unit=unit
    def status(self)->ServiceInfo:
        state={RuntimeState.ACTIVE:ServiceState.RUNNING,RuntimeState.INACTIVE:ServiceState.STOPPED,
               RuntimeState.MISSING:ServiceState.UNAVAILABLE}.get(self.runtime.state(self.unit),ServiceState.UNKNOWN)
        return ServiceInfo(self.service_id,state,self.backend)
    def start(self)->ServiceInfo:self.runtime.start(self.unit);return self.status()
    def stop(self)->ServiceInfo:self.runtime.stop(self.unit);return self.status()
    def restart(self)->ServiceInfo:self.runtime.restart(self.unit);return self.status()

class PounceBackend:
    """pounce bouncer adapter using a dedicated controlled runtime target."""
    backend="pounce"
    def __init__(self,name:str,runtime:Runtime,unit:str="ircsh-pounce.service"):
        self.service_id=ServiceId(ServiceKind.BOUNCER,name);self.runtime=runtime
        if unit!="ircsh-pounce.service":raise ValueError("unsupported pounce runtime unit")
        self.unit=unit
    def status(self)->ServiceInfo:
        state={RuntimeState.ACTIVE:ServiceState.RUNNING,RuntimeState.INACTIVE:ServiceState.STOPPED,
               RuntimeState.MISSING:ServiceState.UNAVAILABLE}.get(self.runtime.state(self.unit),ServiceState.UNKNOWN)
        return ServiceInfo(self.service_id,state,self.backend)
    def start(self)->ServiceInfo:self.runtime.start(self.unit);return self.status()
    def stop(self)->ServiceInfo:self.runtime.stop(self.unit);return self.status()
    def restart(self)->ServiceInfo:self.runtime.restart(self.unit);return self.status()
