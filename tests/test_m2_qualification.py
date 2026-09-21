import tempfile,unittest
from pathlib import Path
from ircsh.config import load_config
from ircsh.services import ServiceKind,ServiceRegistry

class M2QualificationTests(unittest.TestCase):
    def test_defaults_are_read_only(self):
        with tempfile.TemporaryDirectory() as d:
            cfg=load_config(Path(d)/"system.toml",Path(d)/"user.toml")
            self.assertIn("services.read",cfg.account.capabilities)
            self.assertNotIn("bots.manage",cfg.account.capabilities)
            self.assertNotIn("bouncers.manage",cfg.account.capabilities)
            self.assertNotIn("clients.manage",cfg.account.capabilities)
    def test_backend_matrix(self):
        r=ServiceRegistry()
        expected={
          ServiceKind.BOUNCER:{"soju","znc","psybnc","muh","bip","pounce"},
          ServiceKind.BOT:{"eggdrop","limnoria","sopel","errbot","energymech","psotnic"},
          ServiceKind.CLIENT:{"weechat","irssi","bitchx"},
        }
        for kind,names in expected.items():
            self.assertEqual(names,{i.backend for i in r.statuses(kind)})

if __name__=="__main__":unittest.main()
