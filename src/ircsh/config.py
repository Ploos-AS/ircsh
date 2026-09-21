"""M1 configuration loading and validation."""
from __future__ import annotations
import os,tomllib
from dataclasses import dataclass
from pathlib import Path
from .model import Account,KNOWN_CAPABILITIES

DEFAULT_CAPABILITIES=frozenset({"status.read","quota.read","services.read"})

class ConfigError(ValueError): pass

@dataclass(frozen=True,slots=True)
class Config:
    account:Account

def default_paths()->tuple[Path,Path]:
    return Path("/etc/ircsh/config.toml"),Path.home()/".ircsh"/"config.toml"

def _read(path:Path)->dict:
    if not path.exists(): return {}
    try:
        with path.open("rb") as f: return tomllib.load(f)
    except (OSError,tomllib.TOMLDecodeError) as exc:
        raise ConfigError(f"{path}: {exc}") from exc

def load_config(system_path:Path|None=None,user_path:Path|None=None)->Config:
    system_path,user_path=(system_path,user_path) if system_path is not None and user_path is not None else default_paths()
    merged={}
    for data in (_read(system_path),_read(user_path)):
        for key,value in data.items():
            if key!="account": raise ConfigError(f"unknown top-level key: {key}")
            if not isinstance(value,dict): raise ConfigError("account must be a table")
            merged.setdefault("account",{}).update(value)
    account=merged.get("account",{})
    allowed={"name","capabilities"}
    unknown=set(account)-allowed
    if unknown: raise ConfigError(f"unknown account key: {sorted(unknown)[0]}")
    name=account.get("name") or os.environ.get("USER") or "unknown"
    caps=account.get("capabilities",sorted(DEFAULT_CAPABILITIES))
    if not isinstance(name,str) or not name or any(c.isspace() for c in name):
        raise ConfigError("account.name must be a non-empty name without whitespace")
    if not isinstance(caps,list) or not all(isinstance(x,str) for x in caps):
        raise ConfigError("account.capabilities must be an array of strings")
    bad=set(caps)-KNOWN_CAPABILITIES
    if bad: raise ConfigError(f"unknown capability: {sorted(bad)[0]}")
    return Config(Account(name,frozenset(caps)))
