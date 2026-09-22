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
        if path.is_symlink():raise RuntimeError("symlinked configuration rejected")
        if not path.exists():return {}
        result={}
        schema=SCHEMAS[service]
        for line in path.read_text(encoding="utf-8").splitlines():
            if "=" not in line:raise RuntimeError("malformed configuration")
            key,value=line.split("=",1)
            if key in result:raise RuntimeError("duplicate configuration key")
            expected=schema.get(key)
            if expected is None:raise RuntimeError("unknown configuration key")
            if expected is bool:
                if value not in {"true","false"}:raise RuntimeError("malformed boolean")
                parsed=value=="true"
            else:
                parsed=value
            try:self.validate(service,key,parsed)
            except ValueError as exc:raise RuntimeError("invalid stored configuration") from exc
            result[key]=parsed
        return result

    def set(self,service:str,key:str,value:object)->None:
        self.validate(service,key,value)
        path=self._path(service)
        if self.root.is_symlink():raise RuntimeError("symlinked configuration root rejected")
        self.root.mkdir(mode=0o700,parents=True,exist_ok=True)
        os.chmod(self.root,0o700)
        current=self.read(service)
        current[key]=value
        fd,tmp=tempfile.mkstemp(prefix=f".{service}.",dir=self.root,text=True)
        try:
            with os.fdopen(fd,"w",encoding="utf-8") as f:
                for k in sorted(current):
                    v=current[k]
                    rendered="true" if v is True else "false" if v is False else v
                    f.write(f"{k}={rendered}\n")
                f.flush();os.fsync(f.fileno())
            os.chmod(tmp,0o600)
            os.replace(tmp,path)
        except BaseException:
            try:os.unlink(tmp)
            except FileNotFoundError:pass
            raise
