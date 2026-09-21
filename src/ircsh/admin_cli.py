"""Administrator-only CLI for the trusted ircsh account registry."""
from __future__ import annotations
import argparse
from .account_store import AccountStore,ManagedAccount
from .admin_model import get_plan
def build_parser():
 p=argparse.ArgumentParser(prog="ircsh-admin");sp=p.add_subparsers(dest="object",required=True);a=sp.add_parser("account");ap=a.add_subparsers(dest="action",required=True);ap.add_parser("list")
 s=ap.add_parser("show");s.add_argument("username");c=ap.add_parser("create");c.add_argument("username");c.add_argument("--plan",default="irc-basic")
 for n in ("disable","enable"):q=ap.add_parser(n);q.add_argument("username")
 q=ap.add_parser("set-plan");q.add_argument("username");q.add_argument("plan");return p
def execute(argv,store=None):
 ns=build_parser().parse_args(argv);store=store or AccountStore();accounts=store.read()
 if ns.action=="list":return "\n".join(f"{a.username}\t{a.plan}\t{'enabled' if a.enabled else 'disabled'}" for a in sorted(accounts.values(),key=lambda x:x.username)) or "(none)"
 if ns.action=="show":
  if ns.username not in accounts:raise KeyError(ns.username)
  a=accounts[ns.username];return f"username={a.username}\nplan={a.plan}\nenabled={'true' if a.enabled else 'false'}"
 if ns.action=="create":
  if ns.username in accounts:raise ValueError("account already exists")
  store.put(ManagedAccount(ns.username,ns.plan));return f"created {ns.username}"
 if ns.username not in accounts:raise KeyError(ns.username)
 a=accounts[ns.username]
 if ns.action=="disable":store.put(ManagedAccount(a.username,a.plan,False));return f"disabled {a.username}"
 if ns.action=="enable":store.put(ManagedAccount(a.username,a.plan,True));return f"enabled {a.username}"
 if ns.action=="set-plan":get_plan(ns.plan);store.put(ManagedAccount(a.username,ns.plan,a.enabled));return f"updated {a.username} plan={ns.plan}"
 raise ValueError("unsupported admin action")
def main():
 import sys
 try:print(execute(sys.argv[1:]))
 except (ValueError,KeyError,RuntimeError) as exc:print(f"ircsh-admin: {exc}",file=sys.stderr);raise SystemExit(2)
