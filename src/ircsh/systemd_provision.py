"""Generate deterministic systemd drop-ins from trusted M4 policy."""
from __future__ import annotations
import os,tempfile
from pathlib import Path
from .isolation import DEFAULT_POLICY,IsolationPolicy
from .systemd_runtime import SystemdUserRuntime

class SystemdDropInProvisioner:
    def __init__(self,root:Path,policy:IsolationPolicy=DEFAULT_POLICY):
        self.root=root;self.policy=policy
    def render(self,unit:str)->str:
        runtime=SystemdUserRuntime(self.policy)
        runtime._unit(unit)
        lines=["[Service]",*runtime.unit_properties()]
        return "\n".join(lines)+"\n"
    def path(self,unit:str)->Path:
        SystemdUserRuntime(self.policy)._unit(unit)
        return self.root/f"{unit}.d"/"50-ircsh-isolation.conf"
    def write(self,unit:str)->Path:
        path=self.path(unit);path.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
        os.chmod(path.parent,0o700)
        content=self.render(unit)
        fd,tmp=tempfile.mkstemp(prefix=".ircsh-",dir=path.parent,text=True)
        try:
            with os.fdopen(fd,"w",encoding="utf-8") as f:
                f.write(content);f.flush();os.fsync(f.fileno())
            os.chmod(tmp,0o600);os.replace(tmp,path)
        except BaseException:
            try:os.unlink(tmp)
            except FileNotFoundError:pass
            raise
        return path
