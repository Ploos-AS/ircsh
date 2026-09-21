import unittest
from ircsh.cli import Context,execute
from ircsh.config import Config
from ircsh.model import Account
from ircsh.providers import QuotaProvider,ServiceProvider,StatusProvider
from ircsh.session_provider import SessionProvider
from ircsh.sessions import PersistentSession,SessionState

class FakeRuntime:
    def __init__(self):self.current=SessionState.DETACHED
    def state(self,target):return self.current
    def attach(self,target):self.current=SessionState.ATTACHED
    def detach(self,target):self.current=SessionState.DETACHED

def ctx(caps):
    sessions=SessionProvider((PersistentSession("weechat",FakeRuntime()),))
    return Context(Config(Account("test",frozenset(caps))),StatusProvider(),QuotaProvider(),ServiceProvider(),sessions)

class SessionCliTests(unittest.TestCase):
    def test_read_capability(self):
        self.assertEqual("weechat detached",execute("session list",ctx({"sessions.read"}))[0])
        self.assertEqual("weechat detached",execute("session status weechat",ctx({"sessions.read"}))[0])
        self.assertEqual("ircsh: permission denied: sessions.read",execute("session list",ctx(set()))[0])
    def test_manage_capability(self):
        c=ctx({"sessions.manage"})
        self.assertEqual("weechat attached",execute("session attach weechat",c)[0])
        self.assertEqual("weechat detached",execute("session detach weechat",c)[0])
        self.assertEqual("ircsh: permission denied: sessions.manage",execute("session attach weechat",ctx({"sessions.read"}))[0])
    def test_no_injection_or_unknown_session(self):
        out,_=execute("session attach weechat;id",ctx({"sessions.manage"}))
        self.assertEqual("ircsh: session not found: weechat;id",out)

if __name__=="__main__":unittest.main()
