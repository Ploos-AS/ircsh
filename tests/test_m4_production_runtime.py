import unittest
from types import SimpleNamespace
from unittest.mock import patch
from ircsh.cli import context
from ircsh.model import Account
from ircsh.config import Config,ConfigError
from ircsh.services import ServiceKind
class ProductionRuntimeTests(unittest.TestCase):
 @patch("ircsh.cli.HostInspector")
 @patch("ircsh.cli.load_config")
 def test_missing_host_account_fails_closed(self,load,inspector):
  load.return_value=Config(Account("alice",frozenset()))
  inspector.return_value.inspect.return_value=None
  with self.assertRaises(ConfigError):context()
 @patch("ircsh.cli.TmuxSessionRuntime")
 @patch("ircsh.cli.SystemdUserRuntime")
 @patch("ircsh.cli.HostInspector")
 @patch("ircsh.cli.load_config")
 def test_service_registry_uses_quota_runtime(self,load,inspector,systemd,tmux):
  load.return_value=Config(Account("alice",frozenset()))
  inspector.return_value.inspect.return_value=SimpleNamespace(uid=1000,home="/home/alice")
  c=context();backend=c.services.registry.get("main",ServiceKind.BOUNCER)
  self.assertEqual("QuotaRuntime",type(backend.runtime).__name__)
  self.assertIs(systemd.return_value,backend.runtime.runtime)
if __name__=="__main__":unittest.main()
