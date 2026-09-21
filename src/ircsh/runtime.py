"""Controlled runtime interface for service adapters."""
from __future__ import annotations
from enum import Enum
from typing import Protocol

class RuntimeState(str,Enum):
    ACTIVE="active"; INACTIVE="inactive"; MISSING="missing"; UNKNOWN="unknown"

class Runtime(Protocol):
    def state(self,unit:str)->RuntimeState: ...
    def start(self,unit:str)->None: ...
    def stop(self,unit:str)->None: ...
    def restart(self,unit:str)->None: ...

class ReadOnlyRuntime:
    """Default runtime: safe for development, never mutates the host."""
    def state(self,unit:str)->RuntimeState:return RuntimeState.MISSING
    def _deny(self,unit:str)->None:raise PermissionError("runtime mutation disabled")
    start=stop=restart=_deny
