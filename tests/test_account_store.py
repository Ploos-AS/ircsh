import tempfile,unittest
from pathlib import Path
from ircsh.account_store import *
class AccountStoreTests(unittest.TestCase):
 def test_round_trip_and_disable(self):
  with tempfile.TemporaryDirectory() as d:
   s=AccountStore(Path(d)/"accounts.json");s.put(ManagedAccount("alice","irc-basic"))
   self.assertTrue(s.read()["alice"].enabled);s.disable("alice");self.assertFalse(s.read()["alice"].enabled)
   self.assertEqual(0o600,s.path.stat().st_mode&0o777)
 def test_unknown_plan_rejected(self):
  with self.assertRaises(ValueError):ManagedAccount("alice","root")
 def test_corrupt_or_open_schema_fails_closed(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"accounts.json";p.write_text('{"alice":{"plan":"irc-basic","enabled":true,"shell":"/bin/sh"}}')
   with self.assertRaises(RuntimeError):AccountStore(p).read()
 def test_relative_store_rejected(self):
  with self.assertRaises(ValueError):AccountStore(Path("accounts.json"))
if __name__=="__main__":unittest.main()
