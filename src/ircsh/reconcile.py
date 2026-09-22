"""Deterministic drift-aware reconciliation for managed IRC accounts."""
from __future__ import annotations
from dataclasses import dataclass
from .account_store import ManagedAccount
from .provisioning import AccountProvisioning
from .host_inspector import HostAccount
@dataclass(frozen=True,slots=True)
class ReconcileAction:
 argv:tuple[str,...]
 def __post_init__(self):
  if not self.argv or any(type(x) is not str or not x for x in self.argv):raise ValueError("invalid reconcile action")
class AccountReconciler:
 def plan(self,account:ManagedAccount,host:HostAccount|None)->tuple[ReconcileAction,...]:
  p=AccountProvisioning(account.username)
  if host is not None and host.username!=account.username:raise ValueError("host account mismatch")
  if account.enabled:
   if host is None:return (ReconcileAction(("useradd","--create-home","--home-dir",p.home,"--gid",p.group,"--shell",p.shell,"--",p.username)),)
   args=["usermod"]
   if host.group!=p.group:args+=["--gid",p.group]
   if host.home!=p.home:args+=["--home",p.home,"--move-home"]
   if host.shell!=p.shell:args+=["--shell",p.shell]
   return () if len(args)==1 else (ReconcileAction(tuple(args+["--",p.username])),)
  if host is None:return ()
  args=["usermod"]
  if not host.locked:args+=["--lock"]
  if host.shell!="/usr/sbin/nologin":args+=["--shell","/usr/sbin/nologin"]
  return () if len(args)==1 else (ReconcileAction(tuple(args+["--",p.username])),)
