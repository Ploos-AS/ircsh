"""Runtime decorator enforcing trusted account quotas before mutations."""
from __future__ import annotations
from .runtime import RuntimeState

class QuotaRuntime:
    def __init__(self,runtime,meter,enforcer):
        self.runtime=runtime;self.meter=meter;self.enforcer=enforcer
    def state(self,unit:str)->RuntimeState:return self.runtime.state(unit)
    def start(self,unit:str)->None:
        current=self.runtime.state(unit)
        if current is RuntimeState.ACTIVE:return
        if current not in {RuntimeState.INACTIVE,RuntimeState.MISSING}:raise RuntimeError("service state unavailable")
        self.enforcer.allow_service_start(self.meter.read())
        self.runtime.start(unit)
    def stop(self,unit:str)->None:self.runtime.stop(unit)
    def restart(self,unit:str)->None:
        if self.runtime.state(unit) is not RuntimeState.ACTIVE:raise RuntimeError("restart requires active service")
        self.enforcer.check(self.meter.read())
        self.runtime.restart(unit)
