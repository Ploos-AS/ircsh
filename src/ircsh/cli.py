"""Restricted ircsh command environment."""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from collections.abc import Callable
from . import __version__
from .config import Config,ConfigError,load_config
from .providers import QuotaProvider,ServiceProvider,StatusProvider
from .session_provider import SessionProvider\nfrom .tmux_runtime import TmuxSessionRuntime\nfrom .client_sessions import ClientSession
from .service_config import ServiceConfigStore
from .logs import JournalLogProvider
from pathlib import Path

@dataclass(frozen=True,slots=True)
class Context:
    config:Config
    status:StatusProvider
    quota:QuotaProvider
    services:ServiceProvider
    sessions:SessionProvider|None=None
    service_config:ServiceConfigStore|None=None
    logs:JournalLogProvider|None=None

def context()->Context:
    runtime=TmuxSessionRuntime()\n    names=("weechat","irssi","bitchx")\n    sessions=tuple(ClientSession(n,runtime).session for n in names)\n    clients=tuple(ClientSession(n,runtime) for n in names)\n    return Context(load_config(),StatusProvider(),QuotaProvider(),ServiceProvider(),SessionProvider(sessions,clients),ServiceConfigStore(Path.home()/".ircsh"/"services"),JournalLogProvider())

def cmd_help(ctx:Context)->str:
    return """Available commands:
  help          Show this help
  account       Show account identity
  capabilities Show account capabilities
  status        Show account/session status
  services      Show IRC services\n  bot list      List bot instances\n  bot status N  Show bot status\n  bouncer list  List bouncer instances\n  bouncer status N Show bouncer status\n  client list   List persistent IRC clients\n  client status N Show client status
  session list  List persistent sessions
  session status N Show session status
  session start N Start an allowlisted IRC client session
  session attach N Attach a permitted session
  session detach N Detach a permitted session
  config show S Show allowlisted service configuration
  config set S K V Set an allowlisted service configuration value
  logs S [N]    Show up to 200 lines from an allowlisted service log
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
    try: ctx=ctx or context()
    except ConfigError as exc:return f"ircsh: configuration error: {exc}",False
    parts=command.split()
    if parts and parts[0]=="logs":
        if not ctx.config.account.allows("logs.read"):return "ircsh: permission denied: logs.read",False
        if len(parts) not in {2,3}:return f"ircsh: invalid logs command: {command}",False
        try:
            lines=50 if len(parts)==2 else int(parts[2])
            provider=ctx.logs or JournalLogProvider()
            output=provider.read(parts[1],lines)
        except (ValueError,RuntimeError) as exc:return f"ircsh: log operation denied: {exc}",False
        return output or "(empty)",False
    if parts and parts[0]=="config":
        store=ctx.service_config
        if store is None:return "ircsh: configuration store unavailable",False
        if len(parts)==3 and parts[1]=="show":
            if not ctx.config.account.allows("config.read"):return "ircsh: permission denied: config.read",False
            try:data=store.read(parts[2])
            except ValueError as exc:return f"ircsh: config operation denied: {exc}",False
            return "\n".join(f"{k}={str(v).lower() if isinstance(v,bool) else v}" for k,v in sorted(data.items())) or "(empty)",False
        if len(parts)==5 and parts[1]=="set":
            if not ctx.config.account.allows("config.manage"):return "ircsh: permission denied: config.manage",False
            value=parts[4]
            if value in {"true","false"}:value=value=="true"
            try:store.set(parts[2],parts[3],value)
            except (ValueError,OSError) as exc:return f"ircsh: config operation denied: {exc}",False
            return f"{parts[2]} {parts[3]} updated",False
        return f"ircsh: invalid config command: {command}",False
    if parts and parts[0]=="session":
        sessions=ctx.sessions or SessionProvider()
        if len(parts)==2 and parts[1]=="list":
            if not ctx.config.account.allows("sessions.read"):return "ircsh: permission denied: sessions.read",False
            return "\n".join(f"{i.name} {i.state.value}" for i in sessions.read()) or "(none)",False
        if len(parts)==3 and parts[1]=="status":
            if not ctx.config.account.allows("sessions.read"):return "ircsh: permission denied: sessions.read",False
            item=sessions.get(parts[2])
            if not item:return f"ircsh: session not found: {parts[2]}",False
            info=item.status();return f"{info.name} {info.state.value}",False
        if len(parts)==3 and parts[1]=="start":
            if not ctx.config.account.allows("sessions.manage"):return "ircsh: permission denied: sessions.manage",False
            try:info=sessions.start(parts[2])
            except (ValueError,PermissionError,RuntimeError) as exc:return f"ircsh: session operation denied: {exc}",False
            return f"{info.name} {info.state.value}",False
        if len(parts)==3 and parts[1] in {"attach","detach"}:
            if not ctx.config.account.allows("sessions.manage"):return "ircsh: permission denied: sessions.manage",False
            item=sessions.get(parts[2])
            if not item:return f"ircsh: session not found: {parts[2]}",False
            try:info=getattr(item,parts[1])()
            except (PermissionError,RuntimeError) as exc:return f"ircsh: session operation denied: {exc}",False
            return f"{info.name} {info.state.value}",False
        return f"ircsh: invalid session command: {command}",False
    if parts and parts[0]=="bot":
        if len(parts)==2 and parts[1]=="list":
            if not ctx.config.account.allows("bots.read"):return "ircsh: permission denied: bots.read",False
            bots=ctx.services.bots()
            return "\n".join(f"{b.name} {b.backend} {b.state.value}" for b in bots) or "(none)",False
        if len(parts)==3 and parts[1]=="status":
            if not ctx.config.account.allows("bots.read"):return "ircsh: permission denied: bots.read",False
            bot=ctx.services.bot(parts[2])
            if not bot:return f"ircsh: bot not found: {parts[2]}",False
            info=bot.status()
            return f"{info.name} {info.backend} {info.state.value}",False
        if len(parts)==3 and parts[1] in {"start","stop","restart"}:
            if not ctx.config.account.allows("bots.manage"):return "ircsh: permission denied: bots.manage",False
            bot=ctx.services.bot(parts[2])
            if not bot:return f"ircsh: bot not found: {parts[2]}",False
            try: info=getattr(bot,parts[1])()
            except (PermissionError,RuntimeError) as exc:return f"ircsh: bot operation denied: {exc}",False
            return f"{info.name} {info.state.value}",False
        return f"ircsh: invalid bot command: {command}",False
    if parts and parts[0]=="bouncer":
        if len(parts)==2 and parts[1]=="list":
            if not ctx.config.account.allows("bouncers.read"):return "ircsh: permission denied: bouncers.read",False
            items=ctx.services.bouncers()
            return "\n".join(f"{b.name} {b.backend} {b.state.value}" for b in items) or "(none)",False
        if len(parts)==3 and parts[1]=="status":
            if not ctx.config.account.allows("bouncers.read"):return "ircsh: permission denied: bouncers.read",False
            item=ctx.services.bouncer(parts[2])
            if not item:return f"ircsh: bouncer not found: {parts[2]}",False
            info=item.status()
            return f"{info.name} {info.backend} {info.state.value}",False
        if len(parts)==3 and parts[1] in {"start","stop","restart"}:
            if not ctx.config.account.allows("bouncers.manage"):return "ircsh: permission denied: bouncers.manage",False
            item=ctx.services.bouncer(parts[2])
            if not item:return f"ircsh: bouncer not found: {parts[2]}",False
            try: info=getattr(item,parts[1])()
            except (PermissionError,RuntimeError) as exc:return f"ircsh: bouncer operation denied: {exc}",False
            return f"{info.name} {info.state.value}",False
        return f"ircsh: invalid bouncer command: {command}",False
    if parts and parts[0]=="client":
        if len(parts)==2 and parts[1]=="list":
            if not ctx.config.account.allows("clients.read"):return "ircsh: permission denied: clients.read",False
            items=ctx.services.clients()
            return "\n".join(f"{i.name} {i.backend} {i.state.value}" for i in items) or "(none)",False
        if len(parts)==3 and parts[1]=="status":
            if not ctx.config.account.allows("clients.read"):return "ircsh: permission denied: clients.read",False
            item=ctx.services.client(parts[2])
            if not item:return f"ircsh: client not found: {parts[2]}",False
            info=item.status();return f"{info.name} {info.backend} {info.state.value}",False
        if len(parts)==3 and parts[1] in {"start","stop","restart"}:
            if not ctx.config.account.allows("clients.manage"):return "ircsh: permission denied: clients.manage",False
            item=ctx.services.client(parts[2])
            if not item:return f"ircsh: client not found: {parts[2]}",False
            try: info=getattr(item,parts[1])()
            except (PermissionError,RuntimeError) as exc:return f"ircsh: client operation denied: {exc}",False
            return f"{info.name} {info.state.value}",False
        return f"ircsh: invalid client command: {command}",False
    spec=COMMANDS.get(command)
    if spec is None:return f"ircsh: unknown command: {command}",False
    if spec.capability and not ctx.config.account.allows(spec.capability):
        return f"ircsh: permission denied: {spec.capability}",False
    return spec.handler(ctx),False


def interactive(ctx:Context|None=None)->int:
    """Run the restricted interactive command loop."""
    try:
        ctx=ctx or context()
    except ConfigError as exc:
        print(f"ircsh: configuration error: {exc}")
        return 2
    while True:
        try:
            line=input("ircsh> ")
        except (EOFError,KeyboardInterrupt):
            print()
            return 0
        output,done=execute(line,ctx)
        if output: print(output)
        if done:return 0

def main(argv:list[str]|None=None)->int:
    """CLI entry point."""
    parser=argparse.ArgumentParser(prog="ircsh",description="Restricted IRC account shell")
    parser.add_argument("--command","-c",help="execute one ircsh built-in command and exit")
    args=parser.parse_args(argv)
    if args.command is None:return interactive()
    output,_=execute(args.command)
    if output:print(output)
    if output.startswith("ircsh: unknown command:") or output.startswith("ircsh: invalid ") or output.startswith("ircsh: configuration error:"):
        return 2
    if output.startswith("ircsh: permission denied:") or output.startswith("ircsh: ") and " operation denied:" in output:
        return 1
    return 0
