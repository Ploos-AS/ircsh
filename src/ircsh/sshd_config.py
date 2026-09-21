"""Deterministic sshd Match Group policy for IRC-only accounts."""
from __future__ import annotations
import re
from .ssh_policy import DEFAULT_SSH_POLICY,SshPolicy
_GROUP=re.compile(r"^[a-z_][a-z0-9_-]{0,31}$")

def render_match_group(group:str="ircsh",policy:SshPolicy=DEFAULT_SSH_POLICY)->str:
    if not _GROUP.fullmatch(group):raise ValueError("invalid SSH group")
    yesno=lambda v:"yes" if v else "no"
    lines=[
        f"Match Group {group}",
        f"    AllowTcpForwarding {yesno(policy.allow_tcp_forwarding)}",
        f"    AllowAgentForwarding {yesno(policy.allow_agent_forwarding)}",
        f"    X11Forwarding {yesno(policy.allow_x11_forwarding)}",
        f"    PermitTTY {yesno(policy.permit_tty)}",
        f"    PermitUserEnvironment {yesno(policy.permit_user_environment)}",
    ]
    return "\n".join(lines)+"\n"
