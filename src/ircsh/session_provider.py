"""Session provider for restricted persistent client sessions."""
from __future__ import annotations
from .client_sessions import ClientSession
from .sessions import PersistentSession

class SessionProvider:
    def __init__(self,sessions:tuple[PersistentSession,...]|None=None,clients:tuple[ClientSession,...]|None=None):
        self._sessions=sessions or (PersistentSession("weechat"),PersistentSession("irssi"),PersistentSession("bitchx"))
        self._clients={c.spec.name:c for c in (clients or ())}
    def read(self):return tuple(s.status() for s in self._sessions)
    def get(self,name:str):return next((s for s in self._sessions if s.name==name),None)
    def start(self,name:str):
        client=self._clients.get(name)
        if client is None:raise ValueError("unsupported client session")
        return client.start()
