import tempfile,unittest
from pathlib import Path
from ircsh.config import ConfigError,load_config

class ConfigTests(unittest.TestCase):
    def paths(self,system="",user=""):
        d=tempfile.TemporaryDirectory(); root=Path(d.name)
        s=root/"system.toml"; u=root/"user.toml"
        if system: s.write_text(system)
        if user: u.write_text(user)
        return d,s,u

    def test_defaults_are_read_only_capabilities(self):
        d,s,u=self.paths()
        try:
            cfg=load_config(s,u)
            self.assertEqual({"status.read","quota.read","services.read"},set(cfg.account.capabilities))
        finally: d.cleanup()

    def test_user_overrides_account_name(self):
        d,s,u=self.paths('[account]\nname="system"\n','[account]\nname="alice"\n')
        try: self.assertEqual("alice",load_config(s,u).account.name)
        finally: d.cleanup()

    def test_unknown_capability_rejected(self):
        d,s,u=self.paths(user='[account]\ncapabilities=["shell.exec"]\n')
        try:
            with self.assertRaises(ConfigError): load_config(s,u)
        finally: d.cleanup()

    def test_unknown_key_rejected(self):
        d,s,u=self.paths(user='danger=true\n')
        try:
            with self.assertRaises(ConfigError): load_config(s,u)
        finally: d.cleanup()
