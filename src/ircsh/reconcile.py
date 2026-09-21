"""Deterministic privileged reconciliation plan for managed IRC accounts."""
from __future__ import annotations
from dataclasses import dataclass
from collections.abc import Sequence
from .account_store import ManagedAccount
from .provisioning import AccountProvisioning
@dataclass(frozen=True,slots=True)
class ReconcileAction:
 argv:tuple[str,...]
 def __post_init__(self):
  if not self.argv or any(type(x) is not str or not x for x in self.argv):raise ValueError("invalid reconcile action")
class AccountReconciler:
 def plan(self,account:ManagedAccount,exists:bool)->tuple[ReconcileAction,...]:
  if type(exists) is not bool:raise TypeError("exists must be bool")
  p=AccountProvisioning(account.username)
  if account.enabled:
   if not exists:
    return (ReconcileAction(("useradd","--create-home","--home-dir",p.home,"--gid",p.group,"--shell",p.shell,"--",p.username)),)
   return (ReconcileAction(("usermod","--gid",p.group,"--shell",p.shell,"--",p.username)),)
  if not exists:return ()
  return (ReconcileAction(("usermod","--lock","--shell","/usr/sbin/nologin","--",p.username)),)
