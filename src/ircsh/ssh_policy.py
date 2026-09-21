"""Validated SSH deployment policy for ircsh login-shell accounts."""
from __future__ import annotations
from dataclasses import dataclass
import re
_USER=re.compile(r"^[a-z_][a-z0-9_-]{0,31}$")
@dataclass(frozen=True,slots=True)
class SshPolicy:
    allow_tcp_forwarding:bool=False
    allow_agent_forwarding:bool=False
    allow_x11_forwarding:bool=False
    permit_tty:bool=True
    permit_user_environment:bool=False
    def __post_init__(self):
        for n in self.__dataclass_fields__:
            if type(getattr(self,n)) is not bool:raise TypeError(f"{n} must be bool")
DEFAULT_SSH_POLICY=SshPolicy()

def shell_entry(executable:str="/usr/bin/ircsh")->str:
    if executable!="/usr/bin/ircsh":raise ValueError("unsupported ircsh executable")
    return executable

def authorized_key_options(username:str,policy:SshPolicy=DEFAULT_SSH_POLICY)->str:
    if not _USER.fullmatch(username):raise ValueError("invalid account name")
    options=[]
    if not policy.allow_agent_forwarding:options.append("no-agent-forwarding")
    if not policy.allow_tcp_forwarding:options.append("no-port-forwarding")
    if not policy.allow_x11_forwarding:options.append("no-X11-forwarding")
    if not policy.permit_tty:options.append("no-pty")
    options.append(f'restrict')
    return ",".join(options)
