"""Controlled per-service configuration editing for M3.

Only typed, explicitly allowlisted keys can be written beneath a configured
root. Writes use replace semantics so readers never observe partial files.
"""
from __future__ import annotations
import os,re,tempfile
from pathlib import Path

_NAME=re.compile(r"^[A-Za-z0-9_-]+$")
SCHEMAS={
 "weechat":{"autoconnect":bool,"nick":str},
 "irssi":{"autoconnect":bool,"nick":str},
 "bitchx":{"autoconnect":bool,"nick":str},
}

class ServiceConfigStore:
    def __init__(self,root:Path):
        self.root=root

    def _path(self,service:str)->Path:
        if not _NAME.fullmatch(service) or service not in SCHEMAS:raise ValueError("unsupported service")
        return self.root/f"{service}.conf"

    def validate(self,service:str,key:str,value:object)->None:
        schema=SCHEMAS.get(service)
        if schema is None:raise ValueError("unsupported service")
        expected=schema.get(key)
        if expected is None:raise ValueError("unsupported configuration key")
        if type(value) is not expected:raise ValueError("invalid configuration value")
        if isinstance(value,str) and (not value or len(value)>64 or any(c in value for c in "\r\n\0")):
            raise ValueError("invalid configuration value")

    def read(self,service:str)->dict[str,object]:
        path=self._path(service)
        if not path.exists():return {}
        result={}
        schema=SCHEMAS[service]
        for line in path.read_text(encoding="utf-8").splitlines():
            if "=" not in line:continue
            key,value=line.split("=",1)
            expected=schema.get(key)
            if expected is bool and value in {"true","false"}:result[key]=value=="true"
            elif expected is str:result[key]=value
        return result

    def set(self,service:str,key:str,value:object)->None:
        self.validate(service,key,value)
        path=self._path(service)
        self.root.mkdir(mode=0o700,parents=True,exist_ok=True)
        current={}
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                if "=" in line:
                    k,v=line.split("=",1);current[k]=v
        current[key]="true" if value is True else "false" if value is False else value
        fd,tmp=tempfile.mkstemp(prefix=f".{service}.",dir=self.root,text=True)
        try:
            with os.fdopen(fd,"w",encoding="utf-8") as f:
                for k in sorted(current):f.write(f"{k}={current[k]}\n")
                f.flush();os.fsync(f.fileno())
            os.chmod(tmp,0o600)
            os.replace(tmp,path)
        except BaseException:
            try:os.unlink(tmp)
            except FileNotFoundError:pass
            raise
