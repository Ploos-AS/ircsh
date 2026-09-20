"""Restricted ircsh command environment."""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from collections.abc import Callable
from . import __version__
from .config import Config,ConfigError,load_config
from .providers import QuotaProvider,ServiceProvider,StatusProvider

@dataclass(frozen=True,slots=True)
class Context:
    config:Config
    status:StatusProvider
    quota:QuotaProvider
    services:ServiceProvider

def context()->Context:
    return Context(load_config(),StatusProvider(),QuotaProvider(),ServiceProvider())

def cmd_help(ctx:Context)->str:
    return """Available commands:
  help          Show this help
  account       Show account identity
  capabilities Show account capabilities
  status        Show account/session status
  services      Show IRC service placeholders
  quota         Show quota status
  version       Show ircsh version
  exit          Leave ircsh
  quit          Leave ircsh"""

def cmd_account(ctx:Context)->str: return f"Account: {ctx.config.account.name}"
def cmd_capabilities(ctx:Context)->str:
    return "\n".join(sorted(ctx.config.account.capabilities)) or "(none)"
def cmd_status(ctx:Context)->str:
    s=ctx.status.read()
    return f"""ircsh status
Account: {ctx.config.account.name}
Session: {s.session}
Runtime backend: {s.runtime}
Arbitrary OS command execution: disabled"""
def cmd_services(ctx:Context)->str:
    lines=["SERVICE   STATE        AUTOSTART"]
    lines.extend(f"{info.name:<9} {info.state.value:<12} {'yes' if info.autostart else 'no'}" for info in ctx.services.read())
    return "\n".join(lines)
def cmd_quota(ctx:Context)->str: return ctx.quota.read()
def cmd_version(ctx:Context)->str: return f"ircsh {__version__}"

@dataclass(frozen=True,slots=True)
class Command:
    handler:Callable[[Context],str]
    capability:str|None=None

COMMANDS={
 "help":Command(cmd_help),"account":Command(cmd_account),
 "capabilities":Command(cmd_capabilities),
 "status":Command(cmd_status,"status.read"),
 "services":Command(cmd_services,"services.read"),
 "quota":Command(cmd_quota,"quota.read"),"version":Command(cmd_version),
}

def execute(line:str,ctx:Context|None=None)->tuple[str,bool]:
    command=line.strip()
    if not command:return "",False
    if command in {"exit","quit"}:return "",True
    spec=COMMANDS.get(command)
    if spec is None:return f"ircsh: unknown command: {command}",False
    try: ctx=ctx or context()
    except ConfigError as exc:return f"ircsh: configuration error: {exc}",False
    if spec.capability and not ctx.config.account.allows(spec.capability):
        return f"ircsh: permission denied: {spec.capability}",False
    return spec.handler(ctx),False

def interactive()->int:
    try: ctx=context()
    except ConfigError as exc:
        print(f"ircsh: configuration error: {exc}"); return 2
    print(f"ircsh {__version__}")
    print(f"Account: {ctx.config.account.name}")
    print("Purpose-built IRC shell environment")
    print("Type 'help' for available commands.\n")
    while True:
        try: line=input("ircsh> ")
        except (EOFError,KeyboardInterrupt):
            print(); return 0
        output,should_exit=execute(line,ctx)
        if output:print(output)
        if should_exit:return 0

def main(argv:list[str]|None=None)->int:
    parser=argparse.ArgumentParser(prog="ircsh")
    parser.add_argument("--command","-c",help="run one ircsh built-in command and exit")
    args=parser.parse_args(argv)
    if args.command is None:return interactive()
    output,_=execute(args.command)
    if output:print(output)
    return 2 if output.startswith(("ircsh: unknown command:","ircsh: configuration error:","ircsh: permission denied:")) else 0

if __name__=="__main__": raise SystemExit(main())
