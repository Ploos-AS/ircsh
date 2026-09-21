import tempfile,unittest
from pathlib import Path
from ircsh.cli import Context,execute
from ircsh.config import Config
from ircsh.model import Account
from ircsh.providers import QuotaProvider,ServiceProvider,StatusProvider
from ircsh.service_config import ServiceConfigStore

def ctx(caps,root):
    return Context(Config(Account("test",frozenset(caps))),StatusProvider(),QuotaProvider(),ServiceProvider(),None,ServiceConfigStore(root))

class ConfigCliTests(unittest.TestCase):
    def test_set_and_show(self):
        with tempfile.TemporaryDirectory() as d:
            c=ctx({"config.read","config.manage"},Path(d))
            self.assertEqual("weechat nick updated",execute("config set weechat nick tester",c)[0])
            self.assertEqual("nick=tester",execute("config show weechat",c)[0])
            self.assertEqual("weechat autoconnect updated",execute("config set weechat autoconnect true",c)[0])
            self.assertIn("autoconnect=true",execute("config show weechat",c)[0])

    def test_capabilities(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual("ircsh: permission denied: config.read",execute("config show weechat",ctx(set(),Path(d)))[0])
            self.assertEqual("ircsh: permission denied: config.manage",execute("config set weechat nick x",ctx({"config.read"},Path(d)))[0])

    def test_rejects_unknown_and_extra_tokens(self):
        with tempfile.TemporaryDirectory() as d:
            c=ctx({"config.manage"},Path(d))
            self.assertIn("unsupported configuration key",execute("config set weechat command id",c)[0])
            self.assertEqual("ircsh: invalid config command: config set weechat nick ok extra",execute("config set weechat nick ok extra",c)[0])

if __name__=="__main__":unittest.main()
