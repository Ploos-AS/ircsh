"""Persistent terminal-session abstraction for M3.

Session names are validated and mapped to deterministic runtime targets.  The
interface deliberately has no command, executable, or shell parameters.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import re
from typing import Protocol

_NAME=re.compile(r"^[A-Za-z0-9_-]+$")

class SessionState(str,Enum):
    ATTACHED="attached"
    DETACHED="detached"
    MISSING="missing"
    UNKNOWN="unknown"

@dataclass(frozen=True,slots=True)
class SessionInfo:
    name:str
    state:SessionState

class SessionRuntime(Protocol):
    def state(self,target:str)->SessionState: ...
    def attach(self,target:str)->None: ...
    def detach(self,target:str)->None: ...

class ReadOnlySessionRuntime:
    def state(self,target:str)->SessionState:return SessionState.MISSING
    def attach(self,target:str)->None:raise PermissionError("session runtime is read-only")
    def detach(self,target:str)->None:raise PermissionError("session runtime is read-only")

class PersistentSession:
    def __init__(self,name:str,runtime:SessionRuntime|None=None):
        if not _NAME.fullmatch(name):raise ValueError("unsafe session name")
        self.name=name
        self.runtime=runtime or ReadOnlySessionRuntime()
        self.target=f"ircsh-session-{name}"

    def status(self)->SessionInfo:
        return SessionInfo(self.name,self.runtime.state(self.target))

    def attach(self)->SessionInfo:
        self.runtime.attach(self.target)
        return self.status()

    def detach(self)->SessionInfo:
        self.runtime.detach(self.target)
        return self.status()
