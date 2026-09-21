"""Trusted quota usage measurement for M4."""
from __future__ import annotations
import os
from pathlib import Path
from collections.abc import Callable,Iterable
from .quotas import QuotaUsage
from .runtime import RuntimeState

class QuotaMeasurementError(RuntimeError):pass

class QuotaMeter:
    def __init__(self,root:Path,service_units:Iterable[str],runtime,
                 walker:Callable[...,object]=os.walk):
        self.root=root
        self.units=tuple(service_units)
        self.runtime=runtime
        self._walk=walker
        if not self.root.is_absolute():raise ValueError("quota root must be absolute")
        if any(".." in Path(u).parts or "/" in u for u in self.units):raise ValueError("unsafe service unit")
    def disk_mb(self)->int:
        total=0
        try:
            for base,_,files in self._walk(self.root):
                for name in files:
                    path=Path(base)/name
                    try:total+=path.stat().st_size
                    except FileNotFoundError:continue
        except OSError as exc:raise QuotaMeasurementError("disk usage unavailable") from exc
        return (total+(1024*1024-1))//(1024*1024)
    def active_services(self)->int:
        try:return sum(self.runtime.state(u) is RuntimeState.ACTIVE for u in self.units)
        except (OSError,ValueError,RuntimeError) as exc:raise QuotaMeasurementError("service usage unavailable") from exc
    def read(self)->QuotaUsage:
        return QuotaUsage(disk_mb=self.disk_mb(),connections=0,services=self.active_services())
