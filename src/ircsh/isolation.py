"""Typed isolation and quota policy for M4."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class ResourceLimits:
    cpu_percent:int=25
    memory_mb:int=256
    processes:int=64
    disk_mb:int=1024
    connections:int=32
    services:int=4
    def __post_init__(self):
        bounds={"cpu_percent":(1,100),"memory_mb":(32,4096),"processes":(4,512),"disk_mb":(64,102400),"connections":(1,256),"services":(1,32)}
        for name,(low,high) in bounds.items():
            value=getattr(self,name)
            if type(value) is not int or not low<=value<=high:raise ValueError(f"{name} must be {low}..{high}")

@dataclass(frozen=True,slots=True)
class IsolationPolicy:
    limits:ResourceLimits=ResourceLimits()
    private_tmp:bool=True
    protect_home:bool=True
    no_new_privileges:bool=True
    private_devices:bool=True
    restrict_namespaces:bool=True
    def __post_init__(self):
        for name in ("private_tmp","protect_home","no_new_privileges","private_devices","restrict_namespaces"):
            if type(getattr(self,name)) is not bool:raise ValueError(f"{name} must be boolean")

DEFAULT_POLICY=IsolationPolicy()
