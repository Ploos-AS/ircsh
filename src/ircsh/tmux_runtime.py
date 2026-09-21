"""Narrow tmux runtime for persistent ircsh sessions.

Only fixed tmux operations are exposed. Targets must be deterministic ircsh
session names; no shell command, executable, tmux subcommand, or option is
accepted from an account.
"""
from __future__ import annotations
import re
import subprocess
from collections.abc import Callable
from .sessions import SessionState

_TARGET=re.compile(r"^ircsh-session-[A-Za-z0-9_-]+$")

class TmuxSessionRuntime:
    def __init__(self,runner:Callable[...,subprocess.CompletedProcess[str]]|None=None):
        self._run=runner or subprocess.run

    def _target(self,target:str)->str:
        if not _TARGET.fullmatch(target):raise ValueError("unsafe session target")
        return target

    def _exec(self,args:list[str],check:bool=False):
        return self._run(args,capture_output=True,text=True,check=check)

    def state(self,target:str)->SessionState:
        target=self._target(target)
        has=self._exec(["tmux","has-session","-t",target])
        if has.returncode!=0:return SessionState.MISSING
        listed=self._exec(["tmux","list-clients","-t",target])
        if listed.returncode!=0:return SessionState.UNKNOWN
        return SessionState.ATTACHED if listed.stdout.strip() else SessionState.DETACHED

    def attach(self,target:str)->None:
        target=self._target(target)
        if self.state(target) is SessionState.MISSING:
            raise RuntimeError("session does not exist")
        # replace-client avoids exposing a shell or accepting account-controlled
        # tmux arguments; the process becomes the permitted session.
        self._run(["tmux","attach-session","-t",target],check=True)

    def detach(self,target:str)->None:
        target=self._target(target)
        if self.state(target) is SessionState.MISSING:
            raise RuntimeError("session does not exist")
        self._run(["tmux","detach-client","-s",target],check=True)

    def start(self,target:str,argv:tuple[str,...])->None:
        target=self._target(target)
        allowed={("weechat",),("irssi",),("BitchX",)}
        if argv not in allowed:raise ValueError("unsupported client executable")
        if self.state(target) is not SessionState.MISSING:
            raise RuntimeError("session already exists")
        self._run(["tmux","new-session","-d","-s",target,"--",*argv],check=True)
