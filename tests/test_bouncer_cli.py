import unittest
from ircsh.cli import Context,execute
from ircsh.config import Config
from ircsh.model import Account
from ircsh.providers import QuotaProvider,ServiceProvider,StatusProvider
from ircsh.services import PlaceholderBackend,ServiceKind,ServiceRegistry

def ctx(caps):
    r=ServiceRegistry((PlaceholderBackend(ServiceKind.BOUNCER,"main","soju"),PlaceholderBackend(ServiceKind.BOUNCER,"legacy","psybnc")))
    return Context(Config(Account("test",frozenset(caps))),StatusProvider(),QuotaProvider(),ServiceProvider(r))

class BouncerCliTests(unittest.TestCase):
    def test_list_and_status(self):
        out,_=execute("bouncer list",ctx({"bouncers.read"}));self.assertIn("main soju unavailable",out)
        out,_=execute("bouncer status legacy",ctx({"bouncers.read"}));self.assertEqual("legacy psybnc unavailable",out)
    def test_capabilities(self):
        self.assertEqual("ircsh: permission denied: bouncers.read",execute("bouncer list",ctx(set()))[0])
        self.assertEqual("ircsh: permission denied: bouncers.manage",execute("bouncer restart main",ctx({"bouncers.read"}))[0])
    def test_mutation_fails_closed(self):
        self.assertTrue(execute("bouncer restart main",ctx({"bouncers.manage"}))[0].startswith("ircsh: bouncer operation denied:"))
    def test_unknown_and_no_shell_fallback(self):
        self.assertEqual("ircsh: bouncer not found: missing",execute("bouncer status missing",ctx({"bouncers.read"}))[0])
        self.assertIn("not found",execute("bouncer status main;id",ctx({"bouncers.read"}))[0])

if __name__=="__main__":unittest.main()
