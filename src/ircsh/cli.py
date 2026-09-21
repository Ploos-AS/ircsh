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
  services      Show IRC services\n  bot list      List bot instances\n  bot status N  Show bot status\n  bouncer list  List bouncer instances\n  bouncer status N Show bouncer status\n  client list   List persistent IRC clients\n  client status N Show client status
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

