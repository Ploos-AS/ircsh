import tempfile,unittest
from pathlib import Path
from ircsh.account_store import AccountStore
from ircsh.admin_cli import execute
class AdminCliTests(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.store=AccountStore(Path(self.tmp.name)/"accounts.json")
 def tearDown(self):self.tmp.cleanup()
 def test_lifecycle(self):
  self.assertEqual("created alice",execute(["account","create","alice"],self.store));self.assertIn("alice\tirc-basic\tenabled",execute(["account","list"],self.store));self.assertEqual("disabled alice",execute(["account","disable","alice"],self.store));self.assertIn("enabled=false",execute(["account","show","alice"],self.store));self.assertEqual("enabled alice",execute(["account","enable","alice"],self.store));self.assertEqual("updated alice plan=irc-advanced",execute(["account","set-plan","alice","irc-advanced"],self.store))
 def test_fail_closed(self):
  execute(["account","create","alice"],self.store)
  with self.assertRaises(ValueError):execute(["account","create","alice"],self.store)
  with self.assertRaises(ValueError):execute(["account","set-plan","alice","root"],self.store)
if __name__=="__main__":unittest.main()
