"""Minimal M0 interactive shell.

M0 deliberately contains no generic operating-system command execution.
"""

from __future__ import annotations
import argparse
from collections.abc import Callable
from . import __version__

SERVICES = ("soju", "znc", "eggdrop", "weechat", "irssi")

def cmd_help() -> str:
    return """Available commands:
  help       Show this help
  status     Show account/session status
  services   Show IRC service placeholders
  quota      Show quota status
  version    Show ircsh version
  exit       Leave ircsh
  quit       Leave ircsh"""

def cmd_status() -> str:
    return """ircsh status
Session: active
Runtime backend: not configured (M0)
Arbitrary OS command execution: disabled"""

def cmd_services() -> str:
    lines = ["SERVICE   STATE        AUTOSTART"]
    lines.extend(f"{name:<9} unavailable  no" for name in SERVICES)
    return "\n".join(lines)

def cmd_quota() -> str:
    return "Quota backend: not configured (M0)"

def cmd_version() -> str:
    return f"ircsh {__version__}"

COMMANDS: dict[str, Callable[[], str]] = {
    "help": cmd_help, "status": cmd_status, "services": cmd_services,
    "quota": cmd_quota, "version": cmd_version,
}

def execute(line: str) -> tuple[str, bool]:
    command = line.strip()
    if not command:
        return "", False
    if command in {"exit", "quit"}:
        return "", True
    handler = COMMANDS.get(command)
    if handler is None:
        return f"ircsh: unknown command: {command}", False
    return handler(), False

def interactive() -> int:
    print(f"ircsh {__version__}")
    print("Purpose-built IRC shell environment")
    print("Type 'help' for available commands.")
    print()
    while True:
        try:
            line = input("ircsh> ")
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        output, should_exit = execute(line)
        if output:
            print(output)
        if should_exit:
            return 0

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ircsh")
    parser.add_argument("--command", "-c", help="run one ircsh built-in command and exit")
    args = parser.parse_args(argv)
    if args.command is None:
        return interactive()
    output, _ = execute(args.command)
    if output:
        print(output)
    return 0 if not output.startswith("ircsh: unknown command:") else 2

if __name__ == "__main__":
    raise SystemExit(main())
