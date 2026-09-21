"""Runtime decorator enforcing trusted account quotas before mutations."""
from __future__ import annotations
from .audit import AuditEvent,AuditLogger
from .runtime import RuntimeState
class QuotaRuntime:
    def __init__(self,runtime,meter,enforcer,audit=None):
        self.runtime=runtime;self.meter=meter;self.enforcer=enforcer;self.audit=audit or AuditLogger()
    def state(self,unit:str)->RuntimeState:return self.runtime.state(unit)
    def start(self,unit:str)->None:
        current=self.runtime.state(unit)
        if current is RuntimeState.ACTIVE:return
        if current not in {RuntimeState.INACTIVE,RuntimeState.MISSING}:raise RuntimeError("service state unavailable")
        try:self.enforcer.allow_service_start(self.meter.read())
        except Exception as exc:
            self.audit.emit(AuditEvent("service_start",unit,"denied",type(exc).__name__));raise
        try:self.runtime.start(unit)
        except Exception as exc:
            self.audit.emit(AuditEvent("service_start",unit,"failed",type(exc).__name__));raise
        self.audit.emit(AuditEvent("service_start",unit,"allowed"))
    def stop(self,unit:str)->None:
        try:self.runtime.stop(unit)
        except Exception as exc:
            self.audit.emit(AuditEvent("service_stop",unit,"failed",type(exc).__name__));raise
        self.audit.emit(AuditEvent("service_stop",unit,"allowed"))
    def restart(self,unit:str)->None:
        if self.runtime.state(unit) is not RuntimeState.ACTIVE:raise RuntimeError("restart requires active service")
        try:self.enforcer.check(self.meter.read())
        except Exception as exc:
            self.audit.emit(AuditEvent("service_restart",unit,"denied",type(exc).__name__));raise
        try:self.runtime.restart(unit)
        except Exception as exc:
            self.audit.emit(AuditEvent("service_restart",unit,"failed",type(exc).__name__));raise
        self.audit.emit(AuditEvent("service_restart",unit,"allowed"))
