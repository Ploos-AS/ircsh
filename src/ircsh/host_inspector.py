"""Trusted local Unix account inspection for administrative reconciliation."""
from __future__ import annotations
from dataclasses import dataclass
import grp,pwd,spwd
from .ssh_policy import authorized_key_options
@dataclass(frozen=True,slots=True)
class HostAccount:
 username:str;uid:int;gid:int;group:str;home:str;shell:str;locked:bool
class HostInspector:
 def inspect(self,username:str)->HostAccount|None:
  authorized_key_options(username)
  try:p=pwd.getpwnam(username)
  except KeyError:return None
  try:g=grp.getgrgid(p.pw_gid).gr_name
  except KeyError:raise RuntimeError("primary group missing")
  try:password=spwd.getspnam(username).sp_pwdp
  except (KeyError,PermissionError) as exc:raise RuntimeError("shadow account unavailable") from exc
  if type(password) is not str:raise RuntimeError("invalid shadow account")
  locked=password.startswith(("!","*"))
  if type(p.pw_uid) is not int or p.pw_uid<0 or type(p.pw_gid) is not int or p.pw_gid<0:raise RuntimeError("invalid host account")
  for v in (p.pw_dir,p.pw_shell,g):
   if type(v) is not str or not v or any(c in v for c in "\r\n\0"):raise RuntimeError("invalid host account")
  return HostAccount(username,p.pw_uid,p.pw_gid,g,p.pw_dir,p.pw_shell,locked)
