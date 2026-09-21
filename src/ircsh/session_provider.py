"""Session provider for restricted persistent client sessions."""
from __future__ import annotations
from .sessions import PersistentSession

class SessionProvider:
    def __init__(self,sessions:tuple[PersistentSession,...]|None=None):
        self._sessions=sessions or (PersistentSession("weechat"),PersistentSession("irssi"),PersistentSession("bitchx"))
    def read(self):return tuple(s.status() for s in self._sessions)
    def get(self,name:str):return next((s for s in self._sessions if s.name==name),None)
