import unittest
from ircsh.backends import PersistentClientBackend
from ircsh.cli import Context,execute
from ircsh.config import Config
from ircsh.model import Account
from ircsh.providers import QuotaProvider,ServiceProvider,StatusProvider
from ircsh.runtime import RuntimeState
from ircsh.services import ServiceRegistry

class FakeRuntime:
    def __init__(self):self.current=RuntimeState.INACTIVE
    def state(self,u):return self.current
    def start(self,u):self.current=RuntimeState.ACTIVE
    def stop(self,u):self.current=RuntimeState.INACTIVE
    def restart(self,u):self.current=RuntimeState.ACTIVE

def ctx(caps):
    r=ServiceRegistry((PersistentClientBackend("weechat",FakeRuntime(),"weechat"),PersistentClientBackend("irssi",FakeRuntime(),"irssi")))
    return Context(Config(Account("test",frozenset(caps))),StatusProvider(),QuotaProvider(),ServiceProvider(r))

class ClientTests(unittest.TestCase):
    def test_backends_and_units(self):
        self.assertEqual("ircsh-weechat-main.service",PersistentClientBackend("main",FakeRuntime(),"weechat").unit)
        self.assertEqual("ircsh-irssi-main.service",PersistentClientBackend("main",FakeRuntime(),"irssi").unit)
        with self.assertRaises(ValueError):PersistentClientBackend("x",FakeRuntime(),"bash")
    def test_list_status_and_caps(self):
        self.assertIn("weechat weechat inactive",execute("client list",ctx({"clients.read"}))[0])
        self.assertEqual("irssi irssi inactive",execute("client status irssi",ctx({"clients.read"}))[0])
        self.assertEqual("ircsh: permission denied: clients.manage",execute("client start irssi",ctx({"clients.read"}))[0])
    def test_lifecycle(self):
        c=ctx({"clients.manage"})
        self.assertEqual("weechat running",execute("client start weechat",c)[0])
        self.assertEqual("weechat stopped",execute("client stop weechat",c)[0])
    def test_no_shell_fallback(self):
        self.assertIn("not found",execute("client status irssi;id",ctx({"clients.read"}))[0])

if __name__=="__main__":unittest.main()
