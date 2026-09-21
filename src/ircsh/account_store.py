"""Persistent administrator-owned ircsh account registry."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import fcntl,json,os,tempfile
from contextlib import contextmanager
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

 def _check_paths(self)->None:
  if self.path.parent.is_symlink():raise RuntimeError("unsafe account store directory")
  if self.path.is_symlink():raise RuntimeError("unsafe account store")

 @contextmanager
 def _locked(self):
  self.path.parent.mkdir(parents=True,exist_ok=True)
  self._check_paths();os.chmod(self.path.parent,0o700)
  lock=self.path.with_name(self.path.name+".lock")
  if lock.is_symlink():raise RuntimeError("unsafe account store lock")
  fd=os.open(lock,os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW,0o600)
  try:
   os.fchmod(fd,0o600);fcntl.flock(fd,fcntl.LOCK_EX);yield
  finally:
   fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)

 def _read_unlocked(self)->dict[str,ManagedAccount]:
  self._check_paths()
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

 def read(self)->dict[str,ManagedAccount]:
  with self._locked():return self._read_unlocked()

 def _write_unlocked(self,accounts:dict[str,ManagedAccount])->None:
  if type(accounts) is not dict or any(k!=v.username for k,v in accounts.items()):raise ValueError("invalid account mapping")
  self._check_paths()
  payload=json.dumps({k:{"plan":v.plan,"enabled":v.enabled} for k,v in sorted(accounts.items())},sort_keys=True,separators=(",",":"))+"\n"
  fd,tmp=tempfile.mkstemp(prefix=".accounts.",dir=self.path.parent)
  try:
   with os.fdopen(fd,"w",encoding="utf-8") as out:out.write(payload);out.flush();os.fsync(out.fileno())
   os.chmod(tmp,0o600);os.replace(tmp,self.path)
   dfd=os.open(self.path.parent,os.O_RDONLY|os.O_DIRECTORY)
   try:os.fsync(dfd)
   finally:os.close(dfd)
  except Exception:
   try:os.unlink(tmp)
   except OSError:pass
   raise

 def write(self,accounts:dict[str,ManagedAccount])->None:
  with self._locked():self._write_unlocked(accounts)

 def put(self,account:ManagedAccount)->None:
  with self._locked():
   accounts=self._read_unlocked();accounts[account.username]=account;self._write_unlocked(accounts)

 def disable(self,username:str)->None:
  authorized_key_options(username)
  with self._locked():
   accounts=self._read_unlocked()
   if username not in accounts:raise KeyError(username)
   a=accounts[username];accounts[username]=ManagedAccount(a.username,a.plan,False);self._write_unlocked(accounts)
