"""Fixed persistent IRC-client session definitions.

Client executables are selected by trusted code, never by account input.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from .sessions import PersistentSession

class ClientProgram(str,Enum):
    WEECHAT="weechat"
    IRSSI="irssi"
    BITCHX="BitchX"

@dataclass(frozen=True,slots=True)
class ClientSessionSpec:
    name:str
    program:ClientProgram

CLIENT_SESSIONS={
    "weechat":ClientSessionSpec("weechat",ClientProgram.WEECHAT),
    "irssi":ClientSessionSpec("irssi",ClientProgram.IRSSI),
    "bitchx":ClientSessionSpec("bitchx",ClientProgram.BITCHX),
}

class ClientSession:
    def __init__(self,name:str,runtime):
        try:self.spec=CLIENT_SESSIONS[name]
        except KeyError as exc:raise ValueError("unsupported client session") from exc
        self.session=PersistentSession(name,runtime)

    @property
    def target(self):return self.session.target

    @property
    def argv(self)->tuple[str,...]:return (self.spec.program.value,)

    def start(self):
        starter=getattr(self.session.runtime,"start",None)
        if starter is None:raise PermissionError("session runtime cannot start clients")
        starter(self.target,self.argv)
        return self.session.status()
