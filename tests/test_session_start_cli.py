import unittest
from ircsh.cli import Context,execute
from ircsh.client_sessions import ClientSession
from ircsh.config import Config
from ircsh.model import Account
from ircsh.providers import QuotaProvider,ServiceProvider,StatusProvider
from ircsh.session_provider import SessionProvider
from ircsh.sessions import PersistentSession,SessionState

class FakeRuntime:
    def __init__(self):self.current=SessionState.MISSING;self.started=[]
    def state(self,target):return self.current
    def start(self,target,argv):self.started.append((target,argv));self.current=SessionState.DETACHED
    def attach(self,target):self.current=SessionState.ATTACHED
    def detach(self,target):self.current=SessionState.DETACHED

def ctx(caps):
    r=FakeRuntime()
    provider=SessionProvider(
        (PersistentSession("weechat",r),),
        (ClientSession("weechat",r),),
    )
    return Context(Config(Account("test",frozenset(caps))),StatusProvider(),QuotaProvider(),ServiceProvider(),provider),r

class SessionStartCliTests(unittest.TestCase):
    def test_start_requires_manage(self):
        c,_=ctx({"sessions.read"})
        self.assertEqual("ircsh: permission denied: sessions.manage",execute("session start weechat",c)[0])

    def test_start_allowlisted_client(self):
        c,r=ctx({"sessions.manage"})
        self.assertEqual("weechat detached",execute("session start weechat",c)[0])
        self.assertEqual([("ircsh-session-weechat",("weechat",))],r.started)

    def test_cannot_select_executable_or_inject(self):
        c,_=ctx({"sessions.manage"})
        self.assertEqual("ircsh: invalid session command: session start weechat bash",execute("session start weechat bash",c)[0])
        self.assertEqual("ircsh: session operation denied: unsupported client session",execute("session start weechat;id",c)[0])

if __name__=="__main__":unittest.main()
