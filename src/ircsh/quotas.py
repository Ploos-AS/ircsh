"""Fail-closed account quota enforcement for M4."""
from __future__ import annotations
from dataclasses import dataclass
from .isolation import ResourceLimits

@dataclass(frozen=True,slots=True)
class QuotaUsage:
    disk_mb:int=0
    connections:int=0
    services:int=0
    def __post_init__(self):
        for name in ("disk_mb","connections","services"):
            value=getattr(self,name)
            if type(value) is not int or value<0:raise ValueError(f"{name} must be a non-negative integer")

class QuotaExceeded(PermissionError):pass

class QuotaEnforcer:
    def __init__(self,limits:ResourceLimits):self.limits=limits
    def check(self,usage:QuotaUsage)->None:
        checks=(("disk",usage.disk_mb,self.limits.disk_mb),("connections",usage.connections,self.limits.connections),("services",usage.services,self.limits.services))
        for name,value,limit in checks:
            if value>limit:raise QuotaExceeded(f"{name} quota exceeded")
    def allow_service_start(self,usage:QuotaUsage)->None:
        self.check(usage)
        if usage.services>=self.limits.services:raise QuotaExceeded("service quota reached")
    def allow_connection(self,usage:QuotaUsage)->None:
        self.check(usage)
        if usage.connections>=self.limits.connections:raise QuotaExceeded("connection quota reached")
    def allow_disk_growth(self,usage:QuotaUsage,additional_mb:int)->None:
        if type(additional_mb) is not int or additional_mb<0:raise ValueError("additional_mb must be a non-negative integer")
        self.check(usage)
        if usage.disk_mb+additional_mb>self.limits.disk_mb:raise QuotaExceeded("disk quota would be exceeded")
