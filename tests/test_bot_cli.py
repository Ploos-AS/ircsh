import unittest
from ircsh.cli import Context,execute
from ircsh.config import Config
from ircsh.model import Account
from ircsh.providers import QuotaProvider,ServiceProvider,StatusProvider
from ircsh.services import PlaceholderBackend,ServiceKind,ServiceRegistry

def ctx(caps):
    registry=ServiceRegistry((PlaceholderBackend(ServiceKind.BOT,"trivia","eggdrop"),))
    return Context(Config(Account("test",frozenset(caps))),StatusProvider(),QuotaProvider(),ServiceProvider(registry))

class BotCliTests(unittest.TestCase):
    def test_list(self):
        out,_=execute("bot list",ctx({"bots.read"}))
        self.assertIn("trivia eggdrop unavailable",out)
    def test_status(self):
        out,_=execute("bot status trivia",ctx({"bots.read"}))
        self.assertEqual("trivia eggdrop unavailable",out)
    def test_read_capability_required(self):
        out,_=execute("bot list",ctx(set()))
        self.assertEqual("ircsh: permission denied: bots.read",out)
    def test_manage_capability_required(self):
        out,_=execute("bot restart trivia",ctx({"bots.read"}))
        self.assertEqual("ircsh: permission denied: bots.manage",out)
    def test_default_backend_mutation_fails_closed(self):
        out,_=execute("bot restart trivia",ctx({"bots.manage"}))
        self.assertTrue(out.startswith("ircsh: bot operation denied:"))
    def test_unknown_bot(self):
        out,_=execute("bot status missing",ctx({"bots.read"}))
        self.assertEqual("ircsh: bot not found: missing",out)
    def test_no_shell_fallback(self):
        out,_=execute("bot status trivia;id",ctx({"bots.read"}))
        self.assertIn("bot not found",out)

if __name__=="__main__":unittest.main()
