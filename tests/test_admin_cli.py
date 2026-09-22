import tempfile,unittest
from pathlib import Path
from ircsh.account_store import AccountStore
from ircsh.admin_cli import execute
class Sink:
 def __init__(self):self.events=[]
 def emit(self,event):self.events.append(event)
class AdminCliTests(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.store=AccountStore(Path(self.tmp.name)/"accounts.json")
 def tearDown(self):self.tmp.cleanup()
 def test_lifecycle(self):
  self.assertEqual("created alice",execute(["account","create","alice"],self.store));self.assertIn("alice\tirc-basic\tenabled",execute(["account","list"],self.store));self.assertEqual("disabled alice",execute(["account","disable","alice"],self.store));self.assertIn("enabled=false",execute(["account","show","alice"],self.store));self.assertEqual("enabled alice",execute(["account","enable","alice"],self.store));self.assertEqual("updated alice plan=irc-advanced",execute(["account","set-plan","alice","irc-advanced"],self.store))
 def test_enable_disable_are_idempotent_and_audited(self):
  sink=Sink();execute(["account","create","alice"],self.store)
  self.assertEqual("disabled alice",execute(["account","disable","alice"],self.store,audit=sink))
  self.assertEqual("account_disable",sink.events[-1].action)
  count=len(sink.events)
  self.assertEqual("disabled alice (no change)",execute(["account","disable","alice"],self.store,audit=sink))
  self.assertEqual(count,len(sink.events))
  self.assertEqual("enabled alice",execute(["account","enable","alice"],self.store,audit=sink))
  self.assertEqual("account_enable",sink.events[-1].action)
  count=len(sink.events)
  self.assertEqual("enabled alice (no change)",execute(["account","enable","alice"],self.store,audit=sink))
  self.assertEqual(count,len(sink.events))
 def test_fail_closed(self):
  execute(["account","create","alice"],self.store)
  with self.assertRaises(ValueError):execute(["account","create","alice"],self.store)
  with self.assertRaises(ValueError):execute(["account","set-plan","alice","root"],self.store)
if __name__=="__main__":unittest.main()
