"""Trusted local Unix account inspection for administrative reconciliation."""
from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
import grp,pwd
from .ssh_policy import authorized_key_options

def _shadow_password(username:str,path:Path=Path("/etc/shadow"))->str:
 try:lines=path.read_text(encoding="utf-8").splitlines()
 except (OSError,UnicodeError) as exc:raise RuntimeError("shadow account unavailable") from exc
 matches=[]
 for line in lines:
  fields=line.split(":")
  if fields and fields[0]==username:matches.append(fields)
 if len(matches)!=1 or len(matches[0])<2:raise RuntimeError("shadow account unavailable")
 password=matches[0][1]
 if type(password) is not str or any(c in password for c in "\r\n\0"):raise RuntimeError("invalid shadow account")
 return password

@dataclass(frozen=True,slots=True)
class HostAccount:
 username:str;uid:int;gid:int;group:str;home:str;shell:str;locked:bool

class HostInspector:
 def __init__(self,shadow_lookup:Callable[[str],str]|None=None):self._shadow_lookup=shadow_lookup or _shadow_password
 def inspect(self,username:str)->HostAccount|None:
  authorized_key_options(username)
  try:p=pwd.getpwnam(username)
  except KeyError:return None
  try:g=grp.getgrgid(p.pw_gid).gr_name
  except KeyError:raise RuntimeError("primary group missing")
  try:password=self._shadow_lookup(username)
  except RuntimeError:raise
  except Exception as exc:raise RuntimeError("shadow account unavailable") from exc
  if type(password) is not str:raise RuntimeError("invalid shadow account")
  locked=password.startswith(("!","*"))
  if type(p.pw_uid) is not int or p.pw_uid<0 or type(p.pw_gid) is not int or p.pw_gid<0:raise RuntimeError("invalid host account")
  for v in (p.pw_dir,p.pw_shell,g):
   if type(v) is not str or not v or any(c in v for c in "\r\n\0"):raise RuntimeError("invalid host account")
  return HostAccount(username,p.pw_uid,p.pw_gid,g,p.pw_dir,p.pw_shell,locked)
