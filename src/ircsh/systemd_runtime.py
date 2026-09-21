"""Narrow systemd user-runtime adapter for M4."""
from __future__ import annotations
import re,subprocess
from collections.abc import Callable
from .isolation import DEFAULT_POLICY,IsolationPolicy
from .runtime import RuntimeState
_UNIT=re.compile(r"^(?:soju|znc)\.service$|^ircsh-[A-Za-z0-9_-]+\.service$")
class SystemdUserRuntime:
    def __init__(self,policy:IsolationPolicy=DEFAULT_POLICY,runner:Callable[...,subprocess.CompletedProcess[str]]|None=None):
        self.policy=policy;self._run=runner or subprocess.run
    def _unit(self,unit:str)->str:
        if not _UNIT.fullmatch(unit):raise ValueError("unsupported runtime unit")
        return unit
    def _exec(self,args:list[str]):return self._run(args,capture_output=True,text=True,check=False)
    def state(self,unit:str)->RuntimeState:
        unit=self._unit(unit);r=self._exec(["systemctl","--user","is-active",unit])
        if r.returncode==0:return RuntimeState.ACTIVE
        if r.stdout.strip()=="inactive":return RuntimeState.INACTIVE
        if r.stdout.strip() in {"unknown","not-found"} or r.returncode==4:return RuntimeState.MISSING
        return RuntimeState.UNKNOWN
    def _mutate(self,verb:str,unit:str)->None:
        unit=self._unit(unit)
        if verb not in {"start","stop","restart"}:raise ValueError("unsupported runtime operation")
        if self._exec(["systemctl","--user",verb,unit]).returncode!=0:raise RuntimeError("systemd runtime operation failed")
    def start(self,unit:str)->None:self._mutate("start",unit)
    def stop(self,unit:str)->None:self._mutate("stop",unit)
    def restart(self,unit:str)->None:self._mutate("restart",unit)
    def unit_properties(self)->tuple[str,...]:
        p=self.policy;l=p.limits
        return (f"CPUQuota={l.cpu_percent}%",f"MemoryMax={l.memory_mb}M",f"TasksMax={l.processes}",f"PrivateTmp={'yes' if p.private_tmp else 'no'}",f"ProtectHome={'yes' if p.protect_home else 'no'}",f"NoNewPrivileges={'yes' if p.no_new_privileges else 'no'}",f"PrivateDevices={'yes' if p.private_devices else 'no'}",f"RestrictNamespaces={'yes' if p.restrict_namespaces else 'no'}")
