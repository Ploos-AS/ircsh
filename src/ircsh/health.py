"""Machine-readable administrative health and metrics snapshots."""
from __future__ import annotations
from dataclasses import asdict,dataclass
import json
from .account_store import AccountStore
from .host_inspector import HostInspector
from .reconcile import AccountReconciler
@dataclass(frozen=True,slots=True)
class HealthSnapshot:
 ok:bool;accounts:int;enabled:int;disabled:int;drifted:int;missing:int
 def json(self)->str:return json.dumps(asdict(self),sort_keys=True,separators=(",",":"))
class HealthProvider:
 def __init__(self,store=None,inspector=None):self.store=store or AccountStore();self.inspector=inspector or HostInspector()
 def read(self)->HealthSnapshot:
  accounts=self.store.read();enabled=disabled=drifted=missing=0
  for a in accounts.values():
   enabled+=int(a.enabled);disabled+=int(not a.enabled)
   host=self.inspector.inspect(a.username)
   if host is None:missing+=int(a.enabled)
   try:actions=AccountReconciler().plan(a,host)
   except Exception as exc:raise RuntimeError("health reconciliation failed") from exc
   drifted+=int(bool(actions))
  return HealthSnapshot(drifted==0 and missing==0,len(accounts),enabled,disabled,drifted,missing)
