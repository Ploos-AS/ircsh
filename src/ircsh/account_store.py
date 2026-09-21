"""Persistent administrator-owned ircsh account registry."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json,os,tempfile
from .admin_model import get_plan
from .ssh_policy import authorized_key_options
@dataclass(frozen=True,slots=True)
class ManagedAccount:
 username:str
 plan:str
 enabled:bool=True
 def __post_init__(self):
  authorized_key_options(self.username);get_plan(self.plan)
  if type(self.enabled) is not bool:raise TypeError("enabled must be bool")
class AccountStore:
 def __init__(self,path:Path=Path("/var/lib/ircsh/accounts.json")):
  if not path.is_absolute():raise ValueError("account store path must be absolute")
  self.path=path
 def read(self)->dict[str,ManagedAccount]:
  if not self.path.exists():return {}
  try:data=json.loads(self.path.read_text(encoding="utf-8"))
  except (OSError,json.JSONDecodeError) as exc:raise RuntimeError("invalid account store") from exc
  if type(data) is not dict:raise RuntimeError("invalid account store")
  out={}
  try:
   for username,item in data.items():
    if type(item) is not dict or set(item)!={"plan","enabled"}:raise ValueError
    a=ManagedAccount(username,item["plan"],item["enabled"]);out[username]=a
  except (TypeError,ValueError) as exc:raise RuntimeError("invalid account store") from exc
  return out
 def write(self,accounts:dict[str,ManagedAccount])->None:
  if type(accounts) is not dict or any(k!=v.username for k,v in accounts.items()):raise ValueError("invalid account mapping")
  self.path.parent.mkdir(parents=True,exist_ok=True);os.chmod(self.path.parent,0o700)
  payload=json.dumps({k:{"plan":v.plan,"enabled":v.enabled} for k,v in sorted(accounts.items())},sort_keys=True,separators=(",",":"))+"\n"
  fd,tmp=tempfile.mkstemp(prefix=".accounts.",dir=self.path.parent)
  try:
   with os.fdopen(fd,"w",encoding="utf-8") as f:f.write(payload);f.flush();os.fsync(f.fileno())
   os.chmod(tmp,0o600);os.replace(tmp,self.path)
  except Exception:
   try:os.unlink(tmp)
   except OSError:pass
   raise
 def put(self,account:ManagedAccount)->None:
  accounts=self.read();accounts[account.username]=account;self.write(accounts)
 def disable(self,username:str)->None:
  authorized_key_options(username);accounts=self.read()
  if username not in accounts:raise KeyError(username)
  a=accounts[username];accounts[username]=ManagedAccount(a.username,a.plan,False);self.write(accounts)
